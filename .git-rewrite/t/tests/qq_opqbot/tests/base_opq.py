

my_qq = 1281727431 # freaking int!


# it is already inside. so the call fails.
# you might check all friends list and grou list.

lua_v1_api_path = "/v1/LuaApiCaller"

opq_server = {"host":"localhost","port":8780} # this is for arm
# opq_server = {"host":"localhost","port":8781} # this is for amd64
# not 0.0.0.0 but freaking localhost.

# api = ""
# import botoy
from botoy import Action

# qq, port are both int.
# action = Action(port = opq_server["port"], host=opq_server["host"])
action = Action(qq = my_qq, port = opq_server["port"], host=opq_server["host"])
#  	搜索群组 添加好友
# openRedBag 	打开红包
# joinGroup 	加入群聊
# dealFriend 	处理好友请求




import json

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