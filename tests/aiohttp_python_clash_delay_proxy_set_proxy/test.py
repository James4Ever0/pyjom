from download_from_multiple_websites_at_once import concurrentGet
import os

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
    proxyList, port=9911, url="https://deepl.com", debug=False, timeout=3
):  # test the speed for given url
    # first, generate the proper list of requests.
    for proxyName in proxyList:
        testUrl = localhostWithPort(port) + "/proxies/{}/delay".format(proxyName)
        params = {'timeout': timeout, 'url': url}
        r = requests.get(testUrl, params=params)
        # we need to test the non-async version.
        req_json = r.json()
        yield req_json


def setProxy(proxy, port=9911):
    ...


def getConnectionGateway(port=9911):  # get the clash local http proxy connection port.
    ...


if __name__ == "__main__":
    import pprint

    proxyList = getProxyList(debug=True)
    # pprint.pprint(result)
    for result in testProxyList(proxyList):
        print(result)
        # {'message': 'Timeout'}
        # {'message': 'An error occurred in the delay test'}
        breakpoint()