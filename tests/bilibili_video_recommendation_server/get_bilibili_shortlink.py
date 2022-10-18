url = "https://api.bilibili.com/x/share/click"
# url = "https://111.19.247.143/x/share/click"
# is it api.bilibili.com?
# yes, it is.
# use post.
# the damn picture?
# the damn picture is generated. it needs to be uploaded to tencent.

apiUrl ="https://service-ijd4slqi-1253419200.gz.apigw.tencentcs.com/release/short_url"
longUrl = "https://www.bilibili.com/video/BV1Wv41157Wz"
params= {"url":longUrl,"href":"https://xiaojuzi.fun/bili-short-url/"}

import requests

r = requests.get(apiUrl, )