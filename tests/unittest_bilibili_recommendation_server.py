import requests

port = 7341
baseurl = "http://localhost:{}".format(port)

from lazero.network.checker import waitForServerUp

message = "bilibili recommendation server"
waitForServerUp(port, message=message)

# objective = "searchRegisteredVideos"
# objective = "searchVideos"
objective = "searchUserVideos"
# objective = "registerUserVideo"
if objective == "searchVideos":
    params = {
        # "params": {"hop": 1}, # there is no such parameter here.
        # can we pass shit without params?
        "params": ...,
        "query": "hello world",
        "iterate": False,  # not all pages, you dumb fool!
        "page_num": 1,
    }  # check if this works?
elif objective == "searchRegisteredVideos":
    # params = dict(query='hello world') # does not remove ellipsis?
    params = dict(
        query="hello world", tid=..., dedeuserid=..., videoOrder=..., page_num=2
    )  # does not remove ellipsis?
    # print(j)
    # exit()
elif objective == "searchUserVideos":
    # it is good.
    # params = dict(query="猫", method="bm25", videoOrder="click")
    params = dict(query="猫", method="bm25")
    # params = dict(query='猫',method='bm25', dedeuserid=None)
elif objective == "registerUserVideo":
    params = dict(
        bvid="BV1MN4y1P7mq", dedeuserid="397424026", is_mine=True, visible=False
    )
else:
    raise Exception("invalid objective: %s" % objective)


from lazero.utils.json import jsonify

params = jsonify(params)
r = requests.post(baseurl + "/" + objective, json=params)
print("objective: %s" % objective)
print("response:", r.text)
breakpoint()
