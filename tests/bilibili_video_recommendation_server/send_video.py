# botoy can only repost video.
# repostVideo2Group	转发视频到群聊
# repostVideo2Friend	转发视频给好友
# getVideoURL	获取短视频链接

# cqhttp can post video.
# https://docs.go-cqhttp.org/cqcode/#%E7%9F%AD%E8%A7%86%E9%A2%91

baseUrl = "http://0.0.0.0:5700"

group = 543780931

import requests

url = baseUrl + "/send_group_msg"
content = 

message = "[CQ:video,data={}]".format(content) 
data = {"group_id": group, "message": message, "auto_escape": False}
r = requests.post(url, data=data)
print(r.json())
# cannot send json. wtf?
# 请参考 go-cqhttp 端输出
