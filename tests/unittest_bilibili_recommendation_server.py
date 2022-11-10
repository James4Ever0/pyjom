import requests

port = 7341
baseurl = "http://localhost:{}".format(port)

params = {'params':{'hop':1}}
# params = {'params':{'hop':1}}
r = requests.get(baseurl+"/searchVideos", params=params)
print(r.text)
