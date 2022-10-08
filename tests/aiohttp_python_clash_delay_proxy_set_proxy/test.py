from download_from_multiple_websites_at_once import concurrentGet
import os
import json
os.environ["http_proxy"] = ""
os.environ["https_proxy"] = ""
localhost = "http://127.0.0.1"
localhostWithPort = lambda port: "{}:{}".format(localhost, port)
import requests

# so, how do you get the proxy list and test the speed for deepl.com?
def getProxyList(port=9911, debug=False):
    clashUrl = localhostWithPort(port) + "/proxies"  # this will reduce one layer of "/"
    if debug:
        print(clashUrl)
    r = requests.get(clashUrl)
    # return r.content
    proxyInfo = r.json()
    proxyList = [key for key in proxyInfo["proxies"].keys()]
    return proxyList


def testProxyList(
    proxyList,
    port=9911,
    url="https://deepl.com",
    debug=False,
    timeout=3000,  # in miliseconds?
):  # test the speed for given url
    # first, generate the proper list of requests.
    params = {"timeout": timeout, "url": url}
    url_list = [
        localhostWithPort(port) + "/proxies/{}/delay".format(proxyName)
        for proxyName in proxyList
    ]
    return concurrentGet(url_list, processor=lambda x: x.json(), params=params)


def setProxyWithSelector(proxyName, selector='GLOBAL',port=9911):
    clashUrl = localhostWithPort(port) + "/proxies/{}".format(selector)
    r = requests.put(clashUrl,data=json.dumps({"name": proxyName}, ensure_ascii=False).encode())
    try:
        assert r.status_code == 204
    except:
        import traceback
        traceback.print_exc()
        try:
            print(r.content)
            print('error code:', r.status_code)
        print("error when setting proxy with selector"")


def getConnectionGateway(port=9911):  # get the clash local http proxy connection port.
    clashUrl = localhostWithPort(port) + "/configs"
    r = requests.get(clashUrl)
    configs = r.json()
    return configs


if __name__ == "__main__":
    # import pprint
    validProxyDelayList = []
    proxyList = getProxyList(debug=True)
    # pprint.pprint(result)
    delayList = testProxyList(proxyList)
    proxyDelayList = zip(delayList, proxyList)
    for delayDict, proxyName in proxyDelayList:
        if "delay" in delayDict.keys():  # we only get those with valid responses.
            # delay = delayDict["delay"]
            info = delayDict.copy()
            info.update({"name": proxyName})
            validProxyDelayList.append(info)
    validProxyDelayList.sort(key=lambda x: x["delay"])
