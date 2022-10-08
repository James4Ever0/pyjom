from download_from_multiple_websites_at_once import concurrentGet
import os
import json
from typing import Literal, Union
from pprint import pprint

os.environ["http_proxy"] = ""
os.environ["https_proxy"] = ""
localhost = "http://127.0.0.1"
localhostWithPort = lambda port: "{}:{}".format(localhost, port)
import requests

# so, how do you get the proxy list and test the speed for deepl.com?
# if you really want to fall back, just change the proxy config.
def getProxyList(
    port: int = 9911,
    debug=False,
    disallowed_types=["URLTest", "Reject", "Selector", "Direct", "Fallback"],
):  # default do not return proxy groups. only standalone proxies.
    clashUrl = localhostWithPort(port) + "/proxies"  # this will reduce one layer of "/"
    if debug:
        print(clashUrl)
    r = requests.get(clashUrl)
    # return r.content
    proxyInfo = r.json()
    # pprint(proxyInfo)
    proxyList = []
    for proxyName, proxy in proxyInfo["proxies"].items():
        proxyType = proxy["type"]
        # print(proxyType)
        if proxyType not in disallowed_types:
            proxyList.append(proxyName)
    # proxyList = [key for key in proxyInfo["proxies"].keys()]
    return proxyList

def testProxyList(
    proxyList,
    port: int = 9911,
    url="https://deepl.com",
    # debug=False,
    timeout=3000,  # in miliseconds?
):  # test the speed for given url
    # first, generate the proper list of requests.
    params = {"timeout": timeout, "url": url}
    url_list = [
        localhostWithPort(port) + "/proxies/{}/delay".format(proxyName)
        for proxyName in proxyList
    ]
    return concurrentGet(url_list, processor=lambda x: x.json(), params=params)


def setProxyWithSelector(
    proxyName, selector="GLOBAL", port: int = 9911, debug=False
):  # how to make sure it will use 'GLOBAL'? it needs to be done with the config.
    if debug:
        print("select proxy %s with selector %s" % (proxyName, selector))
    clashUrl = localhostWithPort(port) + "/proxies/{}".format(selector)
    r = requests.put(
        clashUrl, data=json.dumps({"name": proxyName}, ensure_ascii=False).encode()
    )
    try:
        assert r.status_code == 204
    except:
        import traceback

        traceback.print_exc()
        try:
            print(r.content)
            print("error code:", r.status_code)
        except:
            ...
        print("error when setting proxy %s with selector %s" % (proxyName, selector))


def setProxyConfig(
    port: int = 9911,
    http_port: Union[None, int] = None,
    mode: Literal[
        "Global", "Rule", "Direct", None
    ] = None,  # currently this mode is configured as 'rule' so everything related to 'deepl' will be redirected.
):
    # https://clash.gitbook.io/doc/restful-api/config
    # sure you can patch more things but that's enough for now.
    clashUrl = localhostWithPort(port) + "/configs"
    configs = {}
    if http_port:
        configs.update({"port": http_port})
    if mode:
        configs.update({"mode": mode})
    r = requests.patch(clashUrl, data=json.dumps(configs, ensure_ascii=False).encode())
    assert r.status_code == 204


def getConnectionGateway(
    port: int = 9911,
):  # get the clash local http proxy connection port.
    clashUrl = localhostWithPort(port) + "/configs"
    r = requests.get(clashUrl)
    configs = r.json()
    http_port = configs["port"]
    gateway = localhostWithPort(http_port)
    return gateway


if __name__ == "__main__":

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
    #     pprint(gateway)
    #     {'allow-lan': True,
    #  'authentication': [],
    #  'bind-address': '*',
    #  'ipv6': False,
    #  'log-level': 'info',
    #  'mixed-port': 0,
    #  'mode': 'rule',
    #  'port': 8381,
    #  'redir-port': 0,
    #  'socks-port': 0,
    #  'tproxy-port': 0}
    gateway = getConnectionGateway()
    print('valid proxies:', len(validProxyDelayList))
    validProxyName = validProxyDelayList[2]["name"]
    setProxyConfig(mode="Global")
    # you can switch to 'Rule' if you want the baidu translation
    setProxyWithSelector(validProxyName, debug=True)
    # now use the proxy!
    r = requests.get("https://deepl.com", proxies={"http": gateway, "https": gateway})
    print()
    print(r.content[:100])
    print(r.status_code)
    print("deepl response")
