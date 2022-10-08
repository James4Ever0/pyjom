from download_from_multiple_websites_at_once import concurrentGet
import pathlib
import os

os.environ["http_proxy"] = ""
os.environ["https_proxy"] = ""
localhost = "http://127.0.0.1"
localhostWithPort = lambda port: "{}:{}".format(localhost, port)
import requests

# so, how do you get the proxy list and test the speed for deepl.com?
def getProxyList(port=9911, debug=False):
    clashUrl = localhostWithPort(port)+"/proxies" # this will reduce one layer of "/"
    if debug:
        print(clashUrl)
    r = requests.get(clashUrl)
    # return r.content
    return r.json()


def testProxyList(
    proxyList, port=9911, url=..., timeout=3
):  # test the speed for given url
    ...


def setProxy(proxy, port=9911):
    ...


def getConnectionGateway(port=9911):  # get the clash local http proxy connection port.
    ...


if __name__ == "__main__":
    import pprint

    result = getProxyList(debug=True)
    pprint.pprint(result)
