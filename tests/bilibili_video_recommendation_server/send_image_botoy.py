# test to broadcast all these things.

from botoy import Action

qq = 917521610
port = 8784
action = Action(qq=qq, port=port, host="127.0.0.1")
user = 1281727431


title_text = "真·朋克！揭秘《赛博朋克2077》屏幕之外的魔幻换弹操作"
content = "{} 观看视频:{}".format(link)
action.sendFriendPic(user=user, picUrl="",content = content)
