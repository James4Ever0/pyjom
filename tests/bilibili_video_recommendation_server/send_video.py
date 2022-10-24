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
import os
# video_path = "big_breast_video.mp4"
# video_path = "sample_video/sample_video.mp4" # this video have some problem. needs intro and outro. need to show some metadata on the way.
video_path = "sample_video/output.mp4" # the 'moderated' video
video_abspath = os.path.abspath(video_path)
content = "file://"+video_abspath

message = "[CQ:video,file={}]".format(content)
data = {"group_id": group, "message": message, "auto_escape": False}
r = requests.post(url, data=data)
print(r.json())
# cannot send json. wtf?
# 请参考 go-cqhttp 端输出
