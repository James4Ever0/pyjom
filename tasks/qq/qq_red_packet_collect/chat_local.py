# local chatbot implemetation.
# first, we need experimental data.

# a unified stack for every group.
# import this shit ahead of everything.
import Levenshtein
import jiagu
import random
from base_opq import stderrPrint


def update_stack(stack, elem, stackSize=300, no_duplicate=True):
    if no_duplicate:
        # check for duplicates.
        if stack == []:
            duplicate = False
        else:
            duplicate = stack[-1] == elem
        if duplicate:
            return stack
    stack += [elem]
    length = len(stack)
    return stack[max(0, length - stackSize) :]


def getSentiment(sentence):
    flag, probability = jiagu.sentiment(sentence)
    # the probability that flag is true.
    return flag, probability


def getAbsSentiment(sentence):  # ignore positive or negative.
    flag, probability = getSentiment(sentence)
    return probability


def getLinearSentiment(sentence):
    flag, probability = getSentiment(sentence)
    if flag == "negative":
        probability = -probability
    return probability


def compareDifference(sent_0, sent_1):
    distance = Levenshtein.distance(sent_0, sent_1)
    return distance


def getRatioDifference(sent_0, sent_1, reverse=False):
    if reverse:
        base_length = len(sent_1)
    else:
        base_length = len(sent_0)
    distance = compareDifference(sent_0, sent_1)
    return min(1, distance / base_length)


def getMinDifference(sent_0, sent_1):
    reverse = False
    if len(sent_0) < len(sent_1):
        reverse = True
    return getRatioDifference(sent_0, sent_1, reverse=reverse)


chat_stack = {}

historicalReplies = []  # should also be a stack.

chat_stack_lock = False


def updateChatStack(group_id, message, stackSize=300, no_duplicate=True):
    chat_stack[group_id] = update_stack(
        chat_stack.get(group_id, []),
        message,
        stackSize=stackSize,
        no_duplicate=no_duplicate,
    )


def sampleChatStack(
    originGroup: int, msg: str, min_corpus_size=100, sample_size=2000, originGroupCut=50
):  # must exclude sent messages.
    # assert min_corpus_size >= sample_size
    # do not do this
    population = [
        (group_id, max(0, len(chat_stack[group_id]) - 1))
        for group_id in chat_stack.keys()
        if group_id != originGroup
    ]

    # population_size = sum([x[1] for x in population]) # wrong.
    population = [  # no need to check against the original group here.
        # if (chat_stack[group_id][index] != msg or group_id != originGroup)
        [
            (group_id, index)
            for index in range(group_msg_size)
            if chat_stack[group_id][index + 1] not in historicalReplies
        ]
        for group_id, group_msg_size in population
    ]  # allow other group with same message or same group with other message
    originGroupLength = len(chat_stack[originGroup]) - 1
    if originGroupLength > originGroupCut:
        # THIS WAS BLOODY WRONG
        # WAS MISPLACED.
        population.append(
            [
                (originGroup, index)
                for index in range(0, originGroupLength - originGroupCut)
                if chat_stack[originGroup][index] != msg
            ]
        )

    population = [x for y in population for x in y]
    population_size = len(population)
    if population_size < min_corpus_size:
        return []
    sample_size = min(population_size, sample_size)
    # it must equal.
    sample = random.sample(population, sample_size)
    return sample


def sentimentFilter(sentiment, threshold=0.85):
    assert threshold > 0 and threshold < 1
    # for too negative ones, we value it as 0.
    if sentiment < -threshold or sentiment > threshold:
        return 0
    return abs(sentiment)


def getChatLocalResponse(
    originGroup: int,
    msg: str,
    min_corpus_size=100,
    sample_size=2000,
    k_top=30,
    originGroupCut=50,
):
    global chat_stack_lock
    # assert min_corpus_size >= sample_size
    if chat_stack_lock:
        return  # do nothing. maybe another thread is holding the lock.
    # must set a global lock.
    chat_stack_lock = True
    sample = sampleChatStack(
        originGroup,
        msg,
        min_corpus_size=min_corpus_size,
        sample_size=sample_size,
        originGroupCut=originGroupCut,
    )
    if len(sample) == 0 or len(sample) != sample_size:  # no sample received.
        chat_stack_lock = False  # release lock
        return
    # this sample must not be empty.
    # rank by Levenshtein distance.
    ranks = [
        (getMinDifference(msg, chat_stack[group_id][gm_index]), index)
        for index, (group_id, gm_index) in enumerate(sample)
    ]
    ranks.sort(key=lambda x: x[0])

    selected_ranks = ranks[:k_top]
    selected_ranks = [sample[index] for difference_score, index in selected_ranks]

    # do we have to match the mood? like positive/negative -> positive/negative?
    # increase the negativity?
    # sentiment shall be next sentence.
    selected_emotional_ranks = [
        (getLinearSentiment(chat_stack[group_id][gm_index + 1]), index)
        for index, (group_id, gm_index) in enumerate(selected_ranks)
    ]
    selected_emotional_ranks.sort(
        key=lambda x: -sentimentFilter(x[0])
    )  # select the extremes. do not select too extreme ones.
    mReplySentiment, mReplyIndex = selected_emotional_ranks[0]
    mReply_group_id, mReply_gm_index = selected_ranks[mReplyIndex]
    mReply = chat_stack[mReply_group_id][mReply_gm_index + 1]  # must plus one.

    # before release lock we need to remove things from chat_stack and append things into historicalReplies(stack)
    update_stack(historicalReplies, mReply)
    # for _ in range(2):
    #     del chat_stack[mReply_group_id][mReply_gm_index] # may cause problems. we might not delete this.
    # discontinuality of message replies.

    # you can somehow make the selected list immutable, into tuple.
    chat_stack_lock = False
    return mReply


# must detect emotion level.
# maybe do sampling on those stacks will help?
# sample size must smaller tha population.
