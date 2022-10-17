url = "https://om.qq.com/image/orginalupload"
# php tencent: http://www.ygbks.com/2501.html gtimg
# python sina: https://www.52pojie.cn/thread-1446200-1-1.html

"""
add something like this in your website
<img src='http://inews.gtimg.com/newsapp_ls/0/14966062446/0' width="200"  referrerpolicy="no-referrer" />
"""
filepath = "test_cover.jpg"
import requests
with open(filepath, "rb") as f:
    content = f.read()
    r = requests.post(url, data=content)
    print(r.status_code)
    # print(r.content)