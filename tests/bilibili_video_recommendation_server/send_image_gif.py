# test to broadcast all these things.


# this method might fail to behave correctly.
# maybe we need to upload the
from botoy import Action

qq = 917521610
port = 8784
action = Action(qq=qq, port=port, host="127.0.0.1")
# user = 1281727431
group = 543780931

link = "https://b23.tv/DPn1G4p"
title_text = "真·朋克！揭秘《赛博朋克2077》屏幕之外的魔幻换弹操作"
content = "观看视频:\n{}\n{}".format(link, title_text)

import base64

# picture_path = "qrcode.gif"
picture_path = "anime_masked_overlay.gif" # how to crop this thing?
# where is the gif? my god?

# there is no way to scan the code in the gif. better send the link instead.
with open(picture_path, "rb") as img_file:
    b64_string = base64.b64encode(img_file.read())
# print(b64_string)
result = action.sendGroupPic(group=group, picBase64Buf=b64_string.decode("utf-8"), content=content)
print(result)
