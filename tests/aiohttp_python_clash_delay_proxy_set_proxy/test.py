from download_from_multiple_websites_at_once import concurrentGet
from lazero.network.proxy.clash import getProxyList, testProxyList, getConnectionGateway

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
