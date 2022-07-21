from botoy import Action
from botoy import Botoy, GroupMsg
import threading
import json
import time
import random
import sys
import traceback

# my_qq = 1281727431 # freaking int! Yukio.
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--qq", type=int, default= 1281727431, required= False) # must not required since we have default value here.
parser.add_argument("--port", type=int, default=8780, required= False)
parser.add_argument("--log", action="store_true")
parser.add_argument("--log_file", action="store_true")

# 忽略信息的blacklist 还有user_blacklist
group_blacklist = [927825838] # 微信的hook发布群
friend_blacklist = [364831018] # 发给我微信hook的人

parsed_args = parser.parse_args()

my_qq = parsed_args.qq
server_port = parsed_args.port
log = parsed_args.log
log_file = parsed_args.log_file

# you can pass the qq via enviorment variable.
# it is already inside. so the call fails.
# you might check all friends list and grou list.
lua_v1_api_path = "/v1/LuaApiCaller"
opq_server = {"host":"localhost","port":server_port} # this is for arm
# opq_server = {"host":"localhost","port":8781} # this is for amd64
# not 0.0.0.0 but freaking localhost.

action = Action(qq = my_qq, port = opq_server["port"], host=opq_server["host"])
bot = Botoy(qq = my_qq, port = opq_server["port"], host=opq_server["host"], log=log,log_file=log_file,group_blacklist=group_blacklist, friend_blacklist=friend_blacklist) # have info. have custom log file.
#  	搜索群组 添加好友
# openRedBag 	打开红包
# joinGroup 	加入群聊
# dealFriend 	处理好友请求


def stderrPrint(*args, **kwargs):
    kwargs.update({"file":sys.stderr})
    print(*args, **kwargs)

def searchGroup(keyword, pageNum=0):
    payload = {"Content":keyword,"Page":pageNum}
    result = action.post(funcname="SearchGroup",payload=payload, path=lua_v1_api_path) # do not pass params since it will auto complete.
    print("SEARCH GROUP RESULT: ", result)
    return result

def addFriend(friend_id, reason="",sourceString="search",group_id=0):
    # some conversions
    if friend_id!=int: friend_id=int(friend_id)
    if group_id!=int: group_id=int(group_id) # source group id.

    add_friend_sources = {"qzone":2011,"search":2020, "group":2004, "discussion":2005}
    source = add_friend_sources[sourceString]
    source_dict = {2011:"空间",2020:"QQ搜索", 2004:"群组", 2005:"讨论组"} # you can make it into another dict.
    assert source in source_dict.keys()
    if source != 2004: group_id = 0 # prevent issues.
    payload = {"Content":reason,"AddFromSource":source,"FromGroupID":group_id,"AddUserUid": friend_id}
    result = action.post(funcname="AddQQUser",payload=payload,path=lua_v1_api_path) # do not pass params since it will auto complete.
    print("ADD FRIEND RESULT: ", result)
    return result

def openRedBag(RedBaginfoDict, group_id, RedBaginfo, delay=(5,10), prefix="[MREDBAG_LOG]"):
    bag_type = RedBaginfoDict["RedType"]
    print(prefix, "THREAD LAUCHED", file=sys.stderr)
    if bag_type in [4, 6, 12]:
        print(prefix,"COLLECTING RED BAG", file=sys.stderr)
        sleep_time = random.randint(*delay)
        print(prefix,"SLEEP TIME:", sleep_time, file=sys.stderr)
        time.sleep(sleep_time)
        title = RedBaginfoDict["Tittle"]
        if bag_type == 12:
            action.sendGroupText(group=group_id, content=title)
        for trial in range(3): # try three times till we get there.
            try:
                answer = action.openRedBag(RedBaginfo)
                print(prefix,"RESULT:", answer, file=sys.stderr)
                print(prefix,"TRIAL %d: COLLECTED RED BAG" % trial, file=sys.stderr)
                assert answer["Ret"] == 0 # assert no problem here.
                break
            except:
                print("_____________RedPacket Exception____________")
                traceback.print_exc()
                print("_____________RedPacket Exception____________")
                sleep_time = random.randint(*delay)
                time.sleep(sleep_time)


def startDaemonThread(target, args=(), kwargs={}):
    thread = threading.Thread(target=target, args=args, kwargs={}, daemon=True)
    thread.start()

def asyncDaemonThread(func):
    def new_func(*args, **kwargs):
        startDaemonThread(func, args=args, kwargs=kwargs)
    return new_func