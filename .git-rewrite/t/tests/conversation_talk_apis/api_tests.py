import urllib.parse
import requests

# disable all proxies.
import os
import time

os.environ["http_proxy"]=""
os.environ["https_proxy"]=""

# do not use freaking proxy, otherwise QingYunKe will not respond.

def checkApi(func,message,name):
    response_message = func(message)
    if response_message!=None:
        print("{} RESPONSE:".format(name), response_message)

def chatAtri(msg: str, BASE='http://api.nekomimi.icu/v1/'):
    url = BASE + 'chat?msg=%s' % msg
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['status'] == 'success':
            return data['message']
    # return None
    # nothing is returned if have error.
    print("ATRI ERROR:", response.status_code, response.json())

# import subprocess
# import json

def chatQingKeYun(msg: str, url="http://api.qingyunke.com/api.php?key=free&appid=0&msg="):
    msg = urllib.parse.quote(msg)
    myUrl = url+msg
    # print(myUrl)
    # output = subprocess.check_output(["curl", myUrl])
    # data = json.loads(output.decode("utf-8"))
    # import requests
    data = requests.get(myUrl)
    data = data.json()
    print(data)
    result = data['result']
    assert result == 0  # 202 -> busy
    content = data['content']
    return content
    # breakpoint()

def xiaobing(msg):
    # 其实是新浪微博群发器 微博群发的逻辑类似于b站群发
    # 刚关注的只能发一条消息
    uid = '5175429989'
    source = '209678993'
    SUB = '_2A25PyitTDeRhGeBG7VAS8y_MwjmIHXVsvhubrDV8PUNbmtANLRfTkW9NRhxXNiVv6Qwut5wwnc8rys3cbJFAxVdX'
    url_send = 'https://api.weibo.com/webim/2/direct_messages/new.json'
    data = {
        'text': msg,
        'uid': uid,
        'source': source
    }
    headers = {
        'cookie': 'SUB='+SUB,
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
        'Referer': 'https://api.weibo.com/chat/'
    }
    response = requests.post(url_send, data=data, headers=headers).json()
    sendMsg = response['text']
    time.sleep(1)
    while True:
        print("RETRYING")
        url_get = 'https://api.weibo.com/webim/2/direct_messages/conversation.json?uid={}&source={}'.format(uid, source)
        response = requests.get(url_get, headers=headers).json()
        getMsg = response['direct_messages'][0]['text']
        if sendMsg == getMsg:
            time.sleep(1)
        else:
            return getMsg

def chatOwnThink(msg:str):
    url = "https://api.ownthink.com/bot?appid=xiaosi&userid=user&spoken="
    msg = urllib.parse.quote(msg)
    myUrl = url+msg
    data = requests.get(myUrl)
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

if __name__ == '__main__':
    # execute my tests.
    message = "你好"
    # checkApi(chatAtri, message, "ATRI")
    # checkApi(xiaobing, message, "XIAOBING")
    # checkApi(chatOwnThink, message, "OWNTHINK")
    checkApi(chatQingKeYun, message, "QINGYUNKE")