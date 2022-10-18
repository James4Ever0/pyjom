url = "https://api.bilibili.com/x/share/click"
# url = "https://111.19.247.143/x/share/click"
# is it api.bilibili.com?
# yes, it is.
# use post.
# the damn picture?
# the damn picture is generated. it needs to be uploaded to tencent.
# url = "https://api.bilibili.com/x/share/click"
burl="https://www.bilibili.com/video/BV1Wv41157Wz"
data = {
    "build": 6700300,
        "buvid": 0,
        "oid": burl,
        "platform": "android",
        "share_channel": "COPY",
        "share_id": "public.webview.0.0.pv",
        "share_mode": 3,
    }
requests.post(url, data=data))["content"]