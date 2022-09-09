import yaml

# target = "https://openit.ml/Clash.yaml"

# import yaml
# import requests
# import os
# os.environ['http_proxy'] = ''
# os.environ['https_proxy'] = ''

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

def jsonLocate(jsonObj,location=[]):
    # print("object:",jsonObj)
    # print("location:",location)
    if location!=[]:
        # try:
        return jsonLocate(jsonObj[location[0]],location[1:])
        # this code is not wrong. it's some shit fucking around.
        # except:
        #     # some shit in jsonObj.
        #     print("SHIT IN jsonObj and location")
        #     print(jsonObj.keys())
        #     print("location:",location)
        #     breakpoint()
    return jsonObj

## FIND DELAY ##
def find_candidates(timeout=6000, urltest="https://m.tujia.com", test_url = "http://localhost:9090/proxies/", location = ["proxies","✋ 手动选择","all"], forbidden_names = ["DIRECT","REJECT","GLOBAL"]):
    

    import requests

    r = requests.get(test_url)

    import json

    data = json.loads(r.text)
    

    proxy_names = jsonLocate(data,location=location)

    # "http://localhost:9090/proxies/DIRECT/delay?timeout=3000&url=https://m.tujia.com"

    def get_delay(name):
        url = "{}{}/delay?timeout={}&url={}".format(test_url, name, timeout, urltest)
        r = requests.get(url)
        response_json = r.text
        response_json = json.loads(response_json)
        if "delay" in response_json.keys(): delay = response_json["delay"]
        else: delay = None
        return delay

    direct_delay = get_delay("DIRECT")
    if direct_delay is None: direct_delay = 300 # approximate delay 300ms

    candidates = []
    import progressbar # 3 minutes.
    for name in progressbar.progressbar([x for x in proxy_names if x not in forbidden_names]):
        # if name in forbidden_names: continue
        # delay = get_delay(name)
        # if delay is not None:
        candidates.append((name,3))
    print("PROXY CANDIDATES: %d" % len(candidates))
    for elem in candidates:
        print(elem)
    return candidates