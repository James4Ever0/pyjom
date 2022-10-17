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
    data = {
        "Filedata": content,
        "subModule": "userAuth_individual_head",
        "id": "FILE_0",
        "name": "test_cover.jpg",
        "type": "image/jpeg",
        # 'lastModifiedDate' : 'Tue Oct 18 03:07:38 GMT+0800 (中国标准时间)',
        "appkey": "1",
        "isRetImgAttr": "1",
        "from": "user",
    }
    r = requests.post(url, data=data)
    print(r.status_code)
    print(r.content)
