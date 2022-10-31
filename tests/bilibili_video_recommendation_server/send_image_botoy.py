# test to broadcast all these things.

# this method might fail to behave correctly.
# maybe we need to upload the image and get url? no thanks?
# we use jpg instead? must use cv2.

# 暂时用不到转发消息的功能

from botoy import Action

qq = 917521610
port = 8784
action = Action(qq=qq, port=port, host="127.0.0.1")
user = 1281727431
import base64

objective = "send_image"

if objective == 'send_video_ad':
    link = "https://b23.tv/DPn1G4p"
    title_text = "真·朋克！揭秘《赛博朋克2077》屏幕之外的魔幻换弹操作"
    content = "观看视频:\n{}\n{}".format(link, title_text)

    picture_path = "ad_2_standalone_cover.png"
    with open(picture_path, "rb") as img_file:
        b64_string = base64.b64encode(img_file.read())
    # print(b64_string)
    result = action.sendFriendPic(user=user, picBase64Buf=b64_string.decode("utf-8"))

    print(result)
    action.sendFriendText(user=user, content=content)
    # send separately.
    # result = action.sendFriendPic(user=user, picBase64Buf=b64_string.decode('utf-8'),content = content)
elif objective == 'send_image':
    # picture_path = "ad_2.png"
    # picture_path = "ebegging_setu_transparent.png"
    picture_path = "image_with_text_8.png"
    with open(picture_path, "rb") as img_file:
        b64_string = base64.b64encode(img_file.read())
    # print(b64_string)
    result = action.sendFriendPic(
        user=user, picBase64Buf=b64_string.decode("utf-8")
    )  # better without content.