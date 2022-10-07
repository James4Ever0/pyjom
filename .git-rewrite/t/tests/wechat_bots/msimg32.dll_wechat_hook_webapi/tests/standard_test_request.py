#encoding: utf-8
import requests
import json
import os
# must force this shit.

#os.system("chcp 65001") # unicode

url_base = "http://localhost:30001/"

def get_url(suffix):return url_base + suffix

def use_api(requested_api, posted_json=None,data=None):
    assert not requested_api.startswith("/")
    url = get_url(requested_api)

    r = requests.post(url,json=posted_json, data=data)

    status_code = r.status_code
    # data_json = r.json()
    data = r.content
    encoding = r.apparent_encoding
    # first we check the freaking encoding.
    with open("sample_response.json","wb") as f: f.write(data)
    print(data, encoding) # gb18030, not gb2312
    decoded_data = data.decode("gb18030")
    data_json = json.loads(decoded_data)
    print("_"*25)
    print("REQUESTED API:",requested_api)
    print("STATUS CODE:",status_code)
    print("DATA JSON:",data_json)
    return data_json

r = use_api("GetFriendAndChatRoomList")

# # target_chat_room = "24471424155@chatroom" # 已经解散 企业微信群
# target_chat_room = "24470228042@chatroom" # 企业微信群
# # target_chat_room = "22652184267@chatroom"
# # target_chat_room = "22502133126@chatroom"
# # data = json.dumps({"gid": target_chat_room}).encode("gb18030")
# r = use_api("BatchGetChatRoomMemberWxid", posted_json={"gid": target_chat_room})# what about the encoding?

r = use_api("TimelineGetFristPage")

r = use_api("GetSelfLoginInfo")
