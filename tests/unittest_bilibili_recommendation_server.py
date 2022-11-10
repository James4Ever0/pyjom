import requests

port = 7341
baseurl = "http://localhost:{}".format(port)

params = {'params':{''}}
r = requests.get(baseurl+"/searchVideos", params=params)
print(r.text)
