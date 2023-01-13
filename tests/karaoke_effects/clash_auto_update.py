import yaml

# you know this source is gone for good.
# target = "https://openit.ml/Clash.yaml"

# import yaml
# import requests
import os

# yes visit this site without any proxy.
os.environ["http_proxy"] = ""
os.environ["https_proxy"] = ""


# CLASH_CONFIG_DOWNLOAD_URL="https://raw.kgithub.com/yu-steven/openit/main/Clash.yaml" # it is down!
# ALL_PROXIES_LOCATION=["proxies", "✋ 手动选择", "all"]
# PROXY_GROUP_EXCEPTIONS = ["👉 例外网站"]
# PROXY_GROUP_SPECIALS =["☁️ 全球直连", "🌐 节点选择"]

# CLASH_CONFIG_DOWNLOAD_URL = "https://subconverter.speedupvpn.com/sub?target=clash&url=https%3A%2F%2Fjsd.cdn.zzko.cn%2Fgh%2FPawdroid%2FFree-servers%40main%2Fsub&insert=false&emoji=true&list=false&tfo=false&scv=false&fdn=false&sort=false&new_name=true" # change this to the direct link you sucker.

import urllib.parse
# DIRECT_LINK = "https://github.com/Pawdroid/Free-servers"
DIRECT_LINK = "https://github.com/Pawdroid/Free-servers/raw/main/sub"

## looking for a clash file merger.
## merge multiple clash files into one.
## evil!

CLASH_CONFIG_DOWNLOAD_URL = f"https://subconverter.speedupvpn.com/sub?target=clash&url={urllib.parse.quote_plus(DIRECT_LINK)}&insert=false&emoji=true&list=false&tfo=false&scv=false&fdn=false&sort=false&new_name=true" # use quote_plus since the slash is not welcomed.

ALL_PROXIES_LOCATION = ["proxies", "🔰 节点选择", "all"]
PROXY_GROUP_EXCEPTIONS = ["🐟 漏网之鱼"]
PROXY_GROUP_SPECIALS = ["🎯 全球直连", "🔰 节点选择", "♻️ 自动选择"]


# r = requests.get(target)
# text = r.text
# json_obj = yaml.safe_load(text)

# port: 7890
# socks5 port: 7891
# controller: http://localhost:9090

# PUT http://localhost:9090/providers/proxies/default
# all_proxies_url = "http://localhost:9090/proxies/"
# one_proxy_url = "http://localhost:9090/proxies/{}".format(proxy_name)
# delay test url: http://localhost:9090/proxies/%F0%9F%87%A8%F0%9F%87%B3%20CN%2014%EF%BD%9Copenit.ml/delay?timeout=2000&url=https://www.baidu.com

from loadSomeCustomClashYaml import goYamlToPyYaml, pyYamlToGoYaml


def jsonLocate(jsonObj, location=[]):
    try:
        if location != []:
            return jsonLocate(jsonObj[location[0]], location[1:])
        return jsonObj
    except:
        print("KEY %s DOES NOT EXIST!", ".".join(location))
        return None


def find_proxy_names(
    test_url="http://localhost:9911/proxies/", location=ALL_PROXIES_LOCATION
):
    import requests

    r = requests.get(test_url)
    import json

    data = json.loads(r.text)
    proxy_names = jsonLocate(data, location=location)
    if proxy_names == None:
        print("SOMEHOW WE FAILED TO FETCH THE PROXY LIST")
        return []
    else:
        return proxy_names


## FIND DELAY ##
def find_tested_proxy_names(
    timeout=3000,
    urltest="https://m.tujia.com",
    test_url="http://localhost:9911/proxies/",
    location=ALL_PROXIES_LOCATION,
    forbidden_names=["DIRECT", "REJECT", "GLOBAL"],
):
    import requests
    import json

    proxy_names = find_proxy_names(test_url, location)
    if proxy_names == []:
        return []

    def get_delay(name):
        url = "{}{}/delay?timeout={}&url={}".format(test_url, name, timeout, urltest)
        r = requests.get(url)
        response_json = r.text
        response_json = json.loads(response_json)
        if "delay" in response_json.keys():
            delay = response_json["delay"]
        else:
            delay = None
        return delay

    direct_delay = get_delay("DIRECT")
    if direct_delay is None:
        direct_delay = 300  # approximate delay 300ms
    candidates = []
    import progressbar  # 3 minutes.

    for name in progressbar.progressbar(
        [x for x in proxy_names if x not in forbidden_names]
    ):
        # if name in forbidden_names: continue
        # delay = get_delay(name)
        # if delay is not None:
        candidates.append((name, 3))
    print("PROXY CANDIDATES: %d" % len(candidates))
    for elem in candidates:
        print(elem)
    return candidates


def setClashProxy(proxy_name, control_port=9911):
    import requests
    import json

    selector = "GLOBAL"
    try:
        r = requests.put(
            "http://localhost:{}/proxies/{}".format(control_port, selector),
            data=json.dumps({"name": proxy_name}, ensure_ascii=False).encode(),
        )
        assert r.status_code == 204
        # assert r.status_code =
    except:
        import traceback

        traceback.print_exc()
        breakpoint()


# with open("ClashBaseOpenIt.yaml", 'r') as f:
#     cachedDNSConfig = yaml.load(f,yaml.FullLoader)


def refineClashYaml(clashYamlPath="Clash3.yaml", advanced=True):
    with open(clashYamlPath, "r") as f:
        data = f.read()
    from loadSomeCustomClashYaml import goYamlToPyYaml, pyYamlToGoYaml

    import yaml

    data = goYamlToPyYaml(data)
    data = yaml.safe_load(data)

    data["port"] = 8381
    base_url = "127.0.0.1:9911"
    data["external-controller"] = base_url
    if "socks-port" in data.keys():
        del data["socks-port"]
    # breakpoint()
    if advanced:
        # print(data['proxies'])
        key = "proxy-groups"
        updatedProxy = []
        updateIndex = 0
        for index, proxy in enumerate(data[key]):
            # breakpoint()
            if proxy["name"] in PROXY_GROUP_EXCEPTIONS:
                # print(proxy)
                # breakpoint()
                updateIndex = index
                updatedProxy = proxy.copy()
                updatedProxy["proxies"] = [
                    elem
                    for elem in proxy["proxies"]
                    if elem not in PROXY_GROUP_SPECIALS
                ]
                updatedProxy["url"] = "https://media4.giphy.com"
                updatedProxy["interval"] = 300
                updatedProxy["tolerance"] = 50
                break
        data[key][updateIndex] = updatedProxy
        # for item in data['proxies']:
        #     print(item)

        # del data["rules"]
        # data["mode"] = "global"
    # data["dns"] = cachedDNSConfig
    data["dns"] = {
        "enable": True,
        "enhanced-mode": "redir-host",
        "fake-ip-filter": ["*.lan", "localhost.ptlogin2.qq.com"],
        "fake-ip-range": "198.18.0.1/16",
        "fallback": [
            "8.8.8.8",
            "1.1.1.1",
            "tls://dns.rubyfish.cn:853",
            "tls://1.0.0.1:853",
            "tls://dns.google:853",
            "https://dns.rubyfish.cn/dns-query",
            "https://cloudflare-dns.com/dns-query",
            "https://dns.google/dns-query",
        ],
        "fallback-filter": {"geoip": True, "ipcidr": ["240.0.0.0/4"]},
        "ipv6": False,
        "listen": "0.0.0.0:61",  # key?
        "nameserver": [
            "223.5.5.5",
            "180.76.76.76",
            "119.29.29.29",
            "117.50.10.10",
            "114.114.114.114",
        ],
    }

    # data = pyYamlToGoYaml(data)
    data_dump = yaml.safe_dump(data, allow_unicode=True)
    data_dump = pyYamlToGoYaml(data_dump)

    with open(clashYamlPath, "w") as f:
        f.write(data_dump)

    """
    import requests
    import json
    base_url =  "http://127.0.0.1:9022"

    url = "/proxies/"
    r = requests.put(base_url+url+"GLOBAL",data=json.dumps({"name":name},ensure_ascii=False).encode())
    assert r.status_code == 204
    """


def getClashYaml(clashYamlPath="Clash3.yaml", url: str = CLASH_CONFIG_DOWNLOAD_URL):
    import requests

    # url = "https://raw.githubusercontents.com/yu-steven/openit/main/Clash.yaml" # some subtle difference!
    # url = 'https://cdn.staticaly.com/gh/yu-steven/openit/main/Clash.yaml'
    # url = "https://raw.kgithub.com/yu-steven/openit/main/Clash.yaml"

    r = requests.get(url)
    with open(clashYamlPath, "w+") as f:
        f.write(r.text)
    print("FETCHING CLASH YAML DONE.")
    print("SAVED AT %s" % clashYamlPath)


from lazero.program import asyncThread


@asyncThread
def updateClashYaml(clashYamlPath="Clash3.yaml", control_port=9911, advanced=True):
    getClashYaml(clashYamlPath=clashYamlPath)
    # if refine:
    refineClashYaml(clashYamlPath=clashYamlPath, advanced=advanced)
    import requests
    import json

    full_config_path = os.path.abspath(clashYamlPath)
    try:
        r = requests.put(
            "http://localhost:{}/configs".format(control_port),
            data=json.dumps({"path": full_config_path}, ensure_ascii=False).encode(),
        )
        # print('REPLY CONTENT:',r.content)
        # breakpoint()
        assert r.status_code == 204
        # might be the problem.
        # TODO: check why the fuck clash server cannot decode the config in utf-8 'unexpected end of data'
        print("SUCCESSFULLY UPDATED THIS PROXY LIST")
        return True
    except:
        import traceback

        traceback.print_exc()
        # breakpoint()
        print("SOME ERROR WHILE FETCHING CLASH OPENIT SCRIPT")
        return False


# this can act as a server as well?
# simplicity in mind.
import schedule

schedule.every(30).minutes.do(updateClashYaml)
updateClashYaml()

from flask import Flask, request

port = 8677

app = Flask(__name__)


def checkProxyExists(proxy):
    return proxy in find_proxy_names()


# from typing import Union


@app.route("/", methods=["GET"])
def serverHello():
    try:
        schedule.run_pending()
    except:
        pass
    return "clash update controller"


@app.route("/checkProxy", methods=["GET"])
def checkProxyAPI():
    proxy = request.args["proxy"]
    print("CHECKING PROXY:", proxy)
    exists = checkProxyExists(proxy)
    return {"exists": exists}


@app.route("/useDirect", methods=["GET"])
def useDirectAPI():
    proxy_name = "DIRECT"
    schedule.run_pending()
    setClashProxy(proxy_name)
    return "refresh proxy to %s" % proxy_name


@app.route("/refreshProxy", methods=["GET"])
def refreshProxyAPI():
    suggest = None
    if "suggest" in request.args.keys():
        suggest = request.args["suggest"]
        print("SUGGESTED PROXY:", suggest)

    schedule.run_pending()
    if suggest:
        if checkProxyExists(suggest):
            setClashProxy(suggest)
            return "refresh suggested proxy to %s" % suggest
    proxy_names = find_proxy_names()
    if proxy_names == []:
        return "failed to find a proxy"
    import random

    proxy_name = random.choice(proxy_names)
    setClashProxy(proxy_name)
    return "refresh proxy to %s" % proxy_name


if __name__ == "__main__":
    app.run(port=port, threaded=True, use_reloader=False)
