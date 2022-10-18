url = "https://api.bilibili.com/x/share/click"
# url = "https://111.19.247.143/x/share/click"
# is it api.bilibili.com?
# yes, it is.
# use post.
# the damn picture?
# the damn picture is generated. it needs to be uploaded to tencent.

apiUrl = "https://service-ijd4slqi-1253419200.gz.apigw.tencentcs.com/release/short_url"
longUrl = "https://www.bilibili.com/video/BV1Wv41157Wz"
import urllib.parse as urlparse
# params = {"url": longUrl}
params = {"url": urlparse.quote(longUrl).replace("/","%2F")}
print(params)
# exit()

headers = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "if-none-match": 'W/"35-oPDNsqBGaZKqGe83GW6wem+lkww"',
    "sec-ch-ua": '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "Referer": "https://xiaojuzi.fun/",
    "Referrer-Policy": "strict-origin-when-cross-origin",
}

import requests

r = requests.get(apiUrl, params=params, headers=headers)
if r.status_code == 200:
    print(r.json())
