from pickle import FALSE
from download_from_multiple_websites_at_once import concurrentGet
import pathlib

localhost = "http://127.0.0.1"
localhostWithPort = lambda port: pathlib.Path("{}:{}".format(localhost, port))
import requests

# so, how do you get the proxy list and test the speed for deepl.com?
def getProxyList(port=9911, debug=FALSE):
    clashUrl = localhostWithPort(port) / "proxies"
    print(clashUrl)

def testProxyList(
    proxyList, port=9911, url=..., timeout=...
):  # test the speed for given url
    ...


def setProxy(proxy, port=9911):
    ...


def getConnectionGateway(port=9911):  # get the clash local http proxy connection port.
    ...

if __name__ == "__main__":
    getProxyList()