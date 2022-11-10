import requests

port = 7341
baseurl = "http://localhost:{}".format(port)

params = {'params':{'hop':1}, 'query'} # check if this works?
# params = {'params':{}}
r = requests.get(baseurl+"/searchVideos", params=params)
print(r.text)
