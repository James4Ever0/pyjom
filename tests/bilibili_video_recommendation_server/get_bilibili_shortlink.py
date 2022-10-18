
apiUrl = "https://service-ijd4slqi-1253419200.gz.apigw.tencentcs.com/release/short_url"
longUrl = "https://www.bilibili.com/video/BV1Wv41157Wz"
import urllib.parse as urlparse
# params = {"url": longUrl}
params = {"url": urlparse.quote(longUrl).replace("/","%2F"), 'href':"https://xiaojuzi.fun/bili-short-url/"}
# print(params)
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
    'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36' # this is important.
}

import requests
request_url = apiUrl+"?url={url}&href={href}".format(**params)
# request_url = 'https://service-ijd4slqi-1253419200.gz.apigw.tencentcs.com/release/short_url?url=https%3A%2F%2Fwww.bilibili.com%2Fvideo%2FBV1Wv41157Wz&href=https://xiaojuzi.fun/bili-short-url/'
# print(request_url)
r = requests.get(request_url, headers=headers)
if r.status_code == 200:
    # print(r.json())
    r_json = r.json()
    success = r_json.get('success', False)
    if success:
        short_url = r_json.get('short_url', None)
        print(short_url)
# starts with 'https://b23.tv'