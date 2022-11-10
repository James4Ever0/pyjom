import requests

port = 7341
baseurl = "http://localhost:{}".format(port)

params = {
    "params": {"hop": 1}, # there is no such parameter here.
    "query": "hello world",
    "iterate": True,
    "page_start": 1,
}  # check if this works?
# params = {'params':{}}

r = requests.post(baseurl + "/searchVideos", params=params)
print("response:", r.text)
