import requests

port = 7341
baseurl = "http://localhost:{}".format(port)

r = requests.get(baseurl+"/searchVideos")
print(r.text)
