import requests

port = 7341
baseurl = "http://localhost:{}".format(port)

from lazero.network.checker import waitForServerUp
message = "bilibili recommendation server"
waitForServerUp(port, message = message)

objective = "searchRegisteredVideos"
if objective == 'searchVideos':
    params = {
        # "params": {"hop": 1}, # there is no such parameter here.
        # can we pass shit without params?
        "params":...,
        "query": "hello world",
        "iterate":False,
        "page_num": 1,
    }  # check if this works?
elif objective == "searchRegisteredVideos":
    # params = dict(query='hello world') # does not remove ellipsis?
    params = dict(query='hello world', tid=..., dedeuserid=..., videoOrder=..., limit=...) # does not remove ellipsis?
    # print(j)
    # exit()
else:
    raise Exception('invalid objective: %s' % objective)


from lazero.utils.json import jsonify
params=jsonify(params)
r = requests.post(baseurl + "/"+objective, json=params)
print('objective: %s' % objective)
print("response:", r.text)
