url = "https://api.bilibili.com/x/share/click"
# url = "https://111.19.247.143/x/share/click"
# is it api.bilibili.com?
# yes, it is.
# use post.
# the damn picture?
# the damn picture is generated. it needs to be uploaded to tencent.
# url = "https://api.bilibili.com/x/share/click"
# burl="https://www.bilibili.com/video/BV1Wv41157Wz"
# burl = "https://www.bilibili.com/v/pay/charge?upmid=85300402&upurl=%2F%2Fspace.bilibili.com%2F85300402&upname=J4D&upavatar=https%3A%2F%2Fi1.hdslb.com%2Fbfs%2Fface%2F73f1323696c857eb5f47f4a8bd03c1115a056af1.jpg&oid=85300402&otype=up&from=zone"
# only from 
# burl = "https://space.bilibili.com/85300402" # my space.
burl = "https://www.bilibili.com/read/cv19232041" # my article with e-begging
data = {
    "build": 6700300,
        "buvid": 0,
        "oid": burl,
        "platform": "android",
        "share_channel": "COPY",
        "share_id": "public.webview.0.0.pv",
        "share_mode": 3,
    }
import requests
headers={'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'}
r=requests.post(url, data=data,headers=headers) # maybe you two share the same user agent!
# we have the link!
if r.status_code == 200:
    # print(r.content)
    r_json=r.json()
    code=r_json["code"]
    if code==0:
        link=r_json["data"]['content']
        print(link)