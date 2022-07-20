import requests
import json
import urllib.parse as up
import sys
# import multithread
from fake_useragent import UserAgent
ua = UserAgent()

user_agent =ua.random

url = "https://v.anime1.me/api"
# data = '{"c":"1019","e":"6b","t":1652428857,"p":0,"s":"ec9042ac177510fd67dd508f4d974074"}'
# data = '%7B%22c%22%3A%221019%22%2C%22e%22%3A%222b%22%2C%22t%22%3A1652429744%2C%22p%22%3A0%2C%22s%22%3A%225a78c05bd07077f05278ed6b44897878%22%7D'
data = "%7B%22c%22%3A%221019%22%2C%22e%22%3A%225b%22%2C%22t%22%3A1652429744%2C%22p%22%3A0%2C%22s%22%3A%222d424b87559a56d7f761c436bca72502%22%7D"
data_unquote = up.unquote(data)
data_json = json.loads(data_unquote)

# url0 = "https://anime1.me/category/2022%e5%b9%b4%e6%98%a5%e5%ad%a3/%e5%8b%87%e8%80%85%e8%be%ad%e8%81%b7%e4%b8%8d%e5%b9%b9%e4%ba%86"
s = requests.Session()

s.headers.update({"User-Agent":user_agent}) # no freaking drama.

# s.get(url0)
# r = requests.post(url,body=data)
mdata = "d={}".format(data)
mheaders = {'authority': 'v.anime1.me'
  ,'accept': '*/*' 
  ,'accept-language': 'en-US,en;q=0.9' 
  ,'content-type': 'application/x-www-form-urlencoded' 
  ,'origin': 'https://anime1.me' 
  ,'referer': 'https://anime1.me/'}
rpost = s.post(url,data=mdata,headers=mheaders)
# print(dir(rpost))
mjson2 = rpost.json()

download_url = mjson2['s']['src']
download_url = "https:"+download_url

download_name = "sample"
download_name = "{}.{}".format(download_name,download_url.split(".")[-1])
# '{"success":false,"errors":["Signature invalid."]}' <- shit.
# breakpoint()
# print(rpost.text) # good. then where is the cookie?
# print(s.cookies)

filename = download_name
# print("downloading target file:",filename)

# download_object = multithread.Downloader(download_url, filename,aiohttp_args= {"headers":mheaders_session}) # ther e is no 'Content-Length'
# download_object.start()
with open(filename, 'wb') as f:
    # response = requests.get(url, stream=True)
    response = s.get(download_url,stream = True)

    total = response.headers.get('content-length')

    if total is None:
        f.write(response.content)
    else:
        downloaded = 0
        total = int(total)
        for data in response.iter_content(chunk_size=max(int(total/1000), 1024*1024)):
            downloaded += len(data)
            f.write(data)
            done = int(50*downloaded/total)
            sys.stdout.write('\r[{}{}]'.format('█' * done, '.' * (50-done)))
            sys.stdout.flush()
sys.stdout.write('\n')
# print(download_content.headers)
# now you have the freaking cookie.
# <RequestsCookieJar[<Cookie e=1652444144 for .v.anime1.me/1019/2b.mp4>, <Cookie h=oRLPqsTE0KXMFmVWJD669g for .v.anime1.me/1019/2b.mp4>, <Cookie p=eyJpc3MiOiJhbmltZTEubWUiLCJleHAiOjE2NTI0NDQxNDQwMDAsImlhdCI6MTY1MjQzNDEzNzAwMCwic3ViIjoiLzEwMTkvMmIubXA0In0 for .v.anime1.me/1019/2b.mp4>]>
# get set-cookie header.