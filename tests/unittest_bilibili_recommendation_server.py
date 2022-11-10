import requests

port = 7341
baseurl = "http://localhost:{}".format(port)

from lazero.network.checker import waitForServerUp
message = "bilibili recommendation server"
waitForServerUp(port, message = message)

if objective == 'searchVideos':
params = {
    # "params": {"hop": 1}, # there is no such parameter here.
    # can we pass shit without params?
    "query": "hello world",
    "iterate": True,
    "page_start": 1,
}  # check if this works?
# r = requests.post(baseurl + , json=params)
# print("response:", r.text)
