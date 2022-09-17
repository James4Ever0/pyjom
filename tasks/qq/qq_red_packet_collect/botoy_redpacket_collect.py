# for arm64 version of opqbot

# disable that 复读机 plugin.
from chat_local import *

from chatApis import getChatApiReply
from base_opq import *
import schedule
from chat_local import getAbsSentiment

from censorApis import censorReplyAbsSentiment
from commons import weightedRandomYielder, generatedSentenceFixer, keywordDecorator, removeDuplicateWords

groupChatCursor = None

groupMsgSendStatus = {}

groupChatReplyHistory = []

groupNoReplyStack = {}  # 防止连续对一个群持续输出

# qq群最多可以添加500个群 1500个好友 其中群可加的数量 = max(0,500 - 已加入群数量 - 好友数量)
# 可以退出一些安静的群 不发红包的群 删除好友

# action.getClusterInfo
# """获取当前集群信息"""
# this is to get the current server running status. i suspect.


def groupMsgRepeater(msg: str, sentiment_threshold=0.7):
    sentiment = getAbsSentiment(msg)
    if sentiment > sentiment_threshold:
        return msg


def checkGroupMsgSendStatus(group_id, decrease=True):
    if group_id in groupMsgSendStatus.keys():
        if decrease:
            groupMsgSendStatus[group_id] -= 1  # the feedback shall be elsewhere.
        if groupMsgSendStatus[group_id] <= 0:
            del groupMsgSendStatus[group_id]
            return True
        else:
            return False
    return True


# now async.
@asyncThread
def sendBotGroupTextMsg(
    replyGetterYielder,
    groupBannedErrorBuffer=100,  # 被禁言之后的buffer
    retry=3,
    min_reply_length=5,  # some impirical value.
    delay_time_range=(5, 15),
    context_size_range=(1, 3),  # maybe we do not need no context. or not?
    maxRepeatRange=(2, 5),
    noReplyThreshold=3,
    noReplyBuffer=75,
):  # the context parameter may lead to OOM.
    global groupChatCursor
    # will clear cursor after sending
    if groupChatCursor is not None:
        # do work here.
        group_id = groupChatCursor["group_id"]
        # groupChatCursor = None
        # return
        result = checkGroupMsgSendStatus(group_id, decrease=False)  # failsafe.
        if not result:
            return

        # modify this textMessage somehow? with context.
        context = random.randint(*context_size_range)
        textMessage = groupChatCursor["msg"]
        groupChatCursorWithContext = groupChatCursor.copy()
        messageContext = chat_stack[group_id][-context:-1] + [
            textMessage
        ]  # include the last message.
        messageContext = " ".join(messageContext)  # just use space.
        groupChatCursorWithContext["msg"] = messageContext

        for (
            replyGetter,
            argumentList,
            flag,
            needContext,
            enableRetryFlag,
        ) in replyGetterYielder:  # use all methods.
            if exit_event.is_set():
                break
            retried = False
            for _ in range(retry):  # retry for three times.
                if exit_event.is_set():
                    break
                extraFlags = {}
                if enableRetryFlag:
                    extraFlags.update({"retryFlag": retried})

                # stderrPrint(extraFlags,replyGetter)

                if needContext:
                    reply = replyGetter(
                        *[groupChatCursorWithContext[key] for key in argumentList],
                        **extraFlags
                    )
                else:
                    reply = replyGetter(
                        *[groupChatCursor[key] for key in argumentList], **extraFlags
                    )
                if reply is not None:
                    retried = True  # only plus one on retryIndex when there is no error during generation.
                    maxRepeat = random.randint(*maxRepeatRange)
                    reply = generatedSentenceFixer(
                        reply, maxRepeat=maxRepeat
                    )  # fix this reply first.
                    # add a new filter here.
                    reply = removeDuplicateWords(reply)
                    if reply in groupChatReplyHistory or len(reply) < min_reply_length:
                        continue  # do not send repeated messages or unusually short messages.
                    else:
                        update_stack(groupChatReplyHistory, reply)
                    # 句子里面不能有违禁词语 不然就不能输出
                    reply = censorReplyAbsSentiment(reply)
                    if reply is None:
                        continue  # skip too vulgar sentences.
                    if reply.count("*") > 3:  # too much censor will make it unreadable.
                        continue  # retry to get a better thing.
                    # do reply.
                    # stderrPrint("PROCESSING GROUP MESSAGE CURSOR:", groupChatCursor)
                    stderrPrint(flag, reply)

                    # must control this shit. 如果被禁言了该如何处理 一般需要缓冲30次
                    groupChatCursor = None  # remove it only one reply was to be made.

                    delay = random.randint(*delay_time_range)
                    time.sleep(delay)  # to make it more humane.

                    sendMessageStatus = action.sendGroupText(
                        group=group_id, content=reply
                    )
                    # stderrPrint("SENT MESSAGE STATUS:",sendMessageStatus)
                    if not (
                        sendMessageStatus["ErrMsg"] == ""
                        and sendMessageStatus["Ret"] == 0
                    ):
                        # some shit had happened. cannot send message without error.
                        groupMsgSendStatus.update({group_id: groupBannedErrorBuffer})
                    else:
                        # no shit happened.
                        groupNoReplyStack.update(
                            {group_id: 1 + groupNoReplyStack.get(group_id, 0)}
                        )
                        # stderrPrint("UPDATE NOREPLYSTACK", groupNoReplyStack)

                        noReply = groupNoReplyStack.get(group_id, 0)
                        if (
                            noReply >= noReplyThreshold
                        ):  # only this noReply greater than 0 we can write it to cursor. LOGIC ELSEWHERE
                            groupNoReplyStack.update({group_id: -noReplyBuffer})

                    # stderrPrint("sendMessageStatus:", sendMessageStatus)

                    return True


def sendRandomGroupMessage():
    sendAtriGroupChatMessage = (
        keywordDecorator(getChatApiReply, chatApiIndex=0),
        ["msg", "group_id"],
        "SENDING ATRI API REPLY:",
        True,
        True,
    )  # last is enableRetryFlag
    sendGPT2GroupChatMessage = (
        keywordDecorator(getChatApiReply, chatApiIndex=1),
        ["msg", "group_id"],
        "SENDING GPT2 API REPLY:",
        True,
        True,
    )  # last is enableRetryFlag
    sendChatLocalResponse = (
        getChatLocalResponse,
        ["group_id", "msg"],
        "SENDING CHATLOCAL REPLY:",
        False,
        False,
    )
    sendRepeaterResponse = (
        groupMsgRepeater,
        ["msg"],
        "SENDING REPEATER REPLY:",
        False,
        False,
    )

    replyGetterList = [
        sendAtriGroupChatMessage,
        sendGPT2GroupChatMessage,
        sendChatLocalResponse,
        sendRepeaterResponse,
    ]
    weightList = [1, 3, 4, 2]
    replyGetterYielder = weightedRandomYielder(replyGetterList, weightList)
    sendBotGroupTextMsg(replyGetterYielder)


# schedule.every(1).minute.do(sendApiGroupChatMessage)
# schedule.every(30).seconds.do(sendChatLocalResponse) # will this shit work?
schedule.every(1).minute.do(sendRandomGroupMessage)  # will this shit work?


def printGroupTextChatJson(group_id, sender_id, content):
    message = {"group_id": group_id, "sender_id": sender_id, "content": content}
    message = json.dumps(message, ensure_ascii=False)
    # stderrPrint("[GROUP_TEXT_MESSAGE]",message)


@bot.on_group_msg
def group(ctx: GroupMsg, groupInitReplyDelayRange=(4, 15)):
    # too broad for groupInitReplyDelayRange to be (2, 20)
    # global groupChatCursor
    #    stderrPrint('收到群消息，群号为', ctx.FromGroupId)
    # recommed you to check the curret group only.
    #    stderrPrint("checkGroupNoReply:",groupNoReplyStack.get(ctx.FromGroupId,None))
    data_dict = ctx.data  # recommend to use this json object. or not?
    group_id = data_dict["FromGroupId"]
    sender_id = data_dict["FromUserId"]
    RedBaginfoDict = data_dict["RedBaginfo"]
    RedBaginfo = ctx.RedBaginfo
    MsgType = ctx.MsgType

    # first initialize random delay for every group in groupNoReplyStack
    if group_id not in groupNoReplyStack.keys():
        groupNoReplyStack.update({group_id: -random.randint(*groupInitReplyDelayRange)})

    def writeGroupChatCursor(Content):
        global groupChatCursor, chat_stack_lock
        # maybe we should create the mapping table here.
        content_length = len(Content)
        content_min_length = 4
        # maybe we should split sentence into shorter ones, or via summarization/title generation apis.
        content_max_length = 15
        recv_content_min_length, recv_content_max_length = 4, 20
        if not (Content.startswith("[") or Content.endswith("]")):
            if (
                content_length <= recv_content_max_length
                and content_length >= recv_content_min_length
            ):
                printGroupTextChatJson(group_id, sender_id, Content) # why the fuck you are not printing?
            if (
                content_length <= content_max_length
                and content_length >= content_min_length
            ):  # 新版qq之类的信息
                # we log group chat text for gpt training here. shall we?
                result = checkGroupMsgSendStatus(group_id)

                if (
                    result
                ):  # will not write banned group to cursor since we will not reply it.
                    noReply = groupNoReplyStack.get(group_id, 0)
                    # stderrPrint("NOREPLYSTACK:",groupNoReplyStack)
                    if noReply >= 0:
                        groupChatCursor = {"group_id": group_id, "msg": Content}
                    else:
                        groupNoReplyStack.update({group_id: noReply + 1})

                # chat_stack update logic within the content length filter
                if chat_stack_lock:
                    # do not do anything about the chat_stack while locked.
                    return
                else:
                    updateChatStack(group_id, Content)
                    # or we could simply add the filter on the reply side.

    if sender_id != my_qq:  # skip text content sent by itself.
        # how to act like the TextMsg? it could include video/image contents.
        if MsgType == "AtMsg":
            Content = ctx.Content  # this is string.
            Content_json = json.loads(Content)
            content_text = Content_json["Content"]
            UserExt = Content_json["UserExt"]
            for elem in UserExt:
                QQNick = elem["QQNick"]
                at_QQNick = "@{}".format(QQNick)
                content_text = content_text.replace(at_QQNick + " " + at_QQNick, "")
                content_text = content_text.replace(at_QQNick, "")
            # now the content is ready.
            writeGroupChatCursor(content_text)
        if MsgType == "TextMsg":
            # is that group allowing sending messages?
            content_text = ctx.Content  # must not be empty.
            writeGroupChatCursor(content_text)

    if RedBaginfoDict is not None:
        prefix = "[MREDBAG_LOG]"
        print(prefix, "RECEIVED RED PACKET", file=sys.stderr)
        print(
            prefix, "_____________RedPacket Message Dump_____________", file=sys.stderr
        )
        print(prefix, ctx, file=sys.stderr)
        print(
            prefix, "_____________RedPacket Message Dump_____________", file=sys.stderr
        )
        startThread(openRedBag, (RedBaginfoDict, group_id, RedBaginfo))
    schedule.run_pending()  # this is async.
    # breakpoint()


if __name__ == "__main__":
    bot.run()

# do not send porn shits or you need to relogin.
