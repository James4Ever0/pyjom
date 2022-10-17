url = "https://om.qq.com/image/orginalupload"
# php tencent: http://www.ygbks.com/2501.html gtimg
# python sina: https://www.52pojie.cn/thread-1446200-1-1.html

"""
add something like this in your website
<img src='http://inews.gtimg.com/newsapp_ls/0/14966062446/0' width="200"  referrerpolicy="no-referrer" />
"""
filePath = "test_cover.jpg"
import requests

# with open(filepath, "rb") as f:
#     content = f.read()
# upload elsewhere.
url = "https://om.qq.com/image/exactupload?relogin=1"
picUrl = "https://open.gtimg.cn/open/app_icon/00/95/17/76/100951776_100_m.png"
url = "https://om.qq.com/image/archscaleupload?isRetImgAttr=1&relogin=1"
files = {
    "Filedata": open(filePath, "rb"),
    "id": "WU_FILE_0",
    "name": "test_cover.jpg",
    "type": "image/jpeg",
    "lastModifiedDate": "10/18/2022, 4:27:08 AM",
    'appKey':'1',
    'isRetImgAttr':'1',
    'from':'user',
    'subModule':'userAuth_individual_head'
}
respone = requests.post(url, files=files,)
res = respone.json()
print(res)
