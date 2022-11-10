import requests

port = 7341
baseurl = "http://localhost:{}".format(port)

from lazero.network.checker import waitForServerUp
message = "bilibili recommendation server"
waitForServerUp(port, message = message)

params = {
    "params": {"hop": 1}, # there is no such parameter here.
    "query": "hello world",
    "iterate": True,
    "page_start": 1,
}  # check if this works?
# params = {'params':{}}

r = requests.post(baseurl + "/searchVideos", data=params)
print("response:", r.text)
