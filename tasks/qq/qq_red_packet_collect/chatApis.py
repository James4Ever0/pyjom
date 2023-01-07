import random
import urllib.parse
import requests
from base_opq import getGroupNameFromDict

# disable all proxies.
import os
import time

os.environ["http_proxy"] = ""
os.environ["https_proxy"] = ""

# do not use freaking proxy, otherwise QingYunKe will not respond.


def checkApi(func, message, name):
    response_message = func(message)
    if response_message != None:
        print("{} RESPONSE:".format(name), response_message)


def chatAtri(
    msg: str, group_id, retryFlag=False, timeout=5, BASE="http://api.nekomimi.icu/v1/"
):
    url = BASE + "chat?msg=%s" % urllib.parse.quote(msg)
    response = requests.get(url, timeout=timeout)
    if response.status_code == 200:
        data = response.json()
        if data["status"] == "success":
            return data["message"]
    # return None
    # nothing is returned if have error.
    print("ATRI ERROR:", response.status_code, response.json())


def chatGPT2Local(
    msg: str, group_id, retryFlag=False, timeout=5, BASE="http://127.0.0.1:8729/"
):
    # url = BASE + '?text=%s' % urllib.parse.quote(msg)
    url = BASE
    params = {"text": msg, "retry": retryFlag, "group_id": group_id}
    response = requests.get(url, params=params)  # simply ignore timeout.
    # response = requests.get(url, timeout=timeout, params = params)
    if response.status_code == 200:
        data = response.text
        if len(data) > 0:
            return data
    # return None
    # nothing is returned if have error.
    print("GPT2LOCAL NO RESPONSE ERROR")  # unknown error.


# import subprocess
# import json


def chatQingKeYun(
    msg: str,
    group_id,
    retryFlag=False,
    timeout=5,
    url="http://api.qingyunke.com/api.php?key=free&appid=0&msg=",
):
    msg = urllib.parse.quote(msg)
    myUrl = url + msg
    # print(myUrl)
    # output = subprocess.check_output(["curl", myUrl])
    # data = json.loads(output.decode("utf-8"))
    # import requests
    data = requests.get(myUrl, timeout=timeout)
    data = data.json()
    print(data)
    result = data["result"]
    assert result == 0  # 202 -> busy
    content = data["content"]
    return content
    # breakpoint()


def chatOwnThink(msg: str, group_id, retryFlag=False, timeout=5):
    url = "https://api.ownthink.com/bot?appid=xiaosi&userid=user&spoken="
    msg = urllib.parse.quote(msg)
    myUrl = url + msg
    data = requests.get(myUrl, timeout=timeout)
    data = data.json()
    # output = subprocess.check_output(["curl", myUrl])
    # data = json.loads(output.decode("utf-8"))
    if data["message"] == "success":
        if data["data"]["type"] == 5000:
            return data["data"]["info"]["text"]

    # print(data)
    # breakpoint()
    # result = data['result']
    # assert result == 0  # 202 -> busy
    # content = data['content']
    # return content


def chatXiaoIce(msg, group_id, retryFlag=False, timeout=5):
    import requests

    topic = getGroupNameFromDict(group_id)
    if topic is None:
        topic = "aaa"  # default topic. nothing.
    r = requests.get(
        "http://localhost:8735/chat",
        params={"topic": topic, "message": msg},
        timeout=timeout,
    )
    if r.status_code == 200:
        try:
            content = r.json()
            assert content["msg"] == "success"
            reply = content["reply"]
            return reply
        except:
            from lazero.utils.logger import traceError

            traceError("xiaoice client error")
    else:
        print("xiaoice client got abnormal response code:", r.status_code)


# changed. non_standard.
def getChatApiReply(
    msg: str, group_id, chatApiIndex=0, retryFlag=False, timeout=15
):  # 15 seconds of grace time.
    # chatApis = [chatQingKeYun, chatAtri]
    # blacklist chatOwnThink.
    chatApis = [chatAtri, chatGPT2Local, chatXiaoIce]  # no random shit!
    # chatApi = random.choice(chatApis)
    chatApi = chatApis[chatApiIndex]
    try:
        reply = chatApi(msg, group_id, retryFlag=retryFlag, timeout=timeout)
        # will be None anyway.
        return reply
    except:
        pass
