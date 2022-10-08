# from download_from_multiple_websites_at_once import concurrentGet
from lazero.network.proxy.clash import (
    getProxyList,
    testProxyList,
    getConnectionGateway,
    setProxyConfig,
    setProxyWithSelector,
)
import requests

if __name__ == "__main__":
    # validProxyDelayList = []
    proxyList = getProxyList(debug=True)
    # pprint.pprint(result)
    validProxyDelayList = testProxyList(proxyList, timeout=5000)
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
    print("valid proxies:", len(validProxyDelayList))
    validProxyName = validProxyDelayList[0]["name"]
    # if no valid proxy, better do another run.
    setProxyConfig(mode="Global")
    # you can switch to 'Rule' if you want the baidu translation
    setProxyWithSelector(validProxyName, debug=True)
    # now use the proxy!
    r = requests.get("https://deepl.com", proxies={"http": gateway, "https": gateway})
    print()
    print(r.content[:100])
    print(r.status_code)
    print("deepl response")
