url = "https://om.qq.com/image/orginalupload"
# php tencent: http://www.ygbks.com/2501.html gtimg
# python sina: https://www.52pojie.cn/thread-1446200-1-1.html

"""
add something like this in your website
<img src='http://inews.gtimg.com/newsapp_ls/0/14966062446/0' width="200"  referrerpolicy="no-referrer" />
"""
filepath = "test_cover.jpg"
import requests

# with open(filepath, "rb") as f:
#     content = f.read()
    # upload elsewhere.
url = 'https://om.qq.com/image/exactupload?relogin=1'
picUrl = "https://open.gtimg.cn/open/app_icon/00/95/17/76/100951776_100_m.png"
data = {'url': picUrl, 'opCode': 151, 'isUpOrg': 1, 'subModule': 'normal_cover'}
response = requests.post(url, data)
res = response.json()
print(res)