from download_from_multiple_websites_at_once import concurrentGet

# so, how do you get the proxy list and test the speed for deepl.com?
def getProxyList(port=...):
    ...

def testProxyList(proxyList,port=..., url=..., timeout=...): # test the speed for given url
    ...

def setProxy(proxy, port=...):
    ...

def getConnectionGateway(port=...): # get the clash local http proxy connection port.