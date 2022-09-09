import yaml

# target = "https://openit.ml/Clash.yaml"

# import yaml
# import requests
import os
os.environ['http_proxy'] = ''
os.environ['https_proxy'] = ''

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

import schedule

def jsonLocate(jsonObj,location=[]):
    try:
        if location!=[]:
            return jsonLocate(jsonObj[location[0]],location[1:])
        return jsonObj
    except:
        print("KEY %s DOES NOT EXIST!", ".".join(location))
        return None

## FIND DELAY ##
def find_candidates(timeout=3000, urltest="https://m.tujia.com", test_url = "http://localhost:9911/proxies/", location = ["proxies","✋ 手动选择","all"], forbidden_names = ["DIRECT","REJECT","GLOBAL"]):
    import requests
    r = requests.get(test_url)
    import json
    data = json.loads(r.text)
    proxy_names = jsonLocate(data,location=location)
    if proxy_names == None:
        print("SOMEHOW WE FAILED TO FETCH THE PROXY LIST")
        return []
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

def setClashProxy(proxy_name,control_port = 9911):
    import requests
    import json
    selector = "GLOBAL"
    try:
        r = requests.put("http://localhost:{}/proxies/{}".format(control_port,selector),data=json.dumps({"name":proxy_name},ensure_ascii=False).encode())
        assert r.status_code == 204
        # assert r.status_code = 
    except:
        import traceback
        traceback.print_exc()
        breakpoint()

def refineClashYaml(clashYamlPath = "Clash3.yaml"):
    with open(clashYamlPath,"r") as f: data = f.read()
    from loadSomeCustomClashYaml import goYamlToPyYaml, pyYamlToGoYaml

    import yaml
    data = goYamlToPyYaml(data)
    data = yaml.safe_load(data)

    data["port"] = 8381
    base_url = "127.0.0.1:9911"
    data["external-controller"]= base_url
    if 'socks-port' in data.keys(): del data["socks-port"]

    del data["rules"]
    data["mode"] = "global"
    data["dns"]["listen"] = "0.0.0.0:{}".format(61)

    # data = pyYamlToGoYaml(data)
    data_dump = yaml.safe_dump(data, allow_unicode=True)
    data_dump =  pyYamlToGoYaml(data_dump)


    with open(clashYamlPath, "w") as f: f.write(data_dump)

    """
    import requests
    import json
    base_url =  "http://127.0.0.1:9022"

    url = "/proxies/"
    r = requests.put(base_url+url+"GLOBAL",data=json.dumps({"name":name},ensure_ascii=False).encode())
    assert r.status_code == 204
    """

def getClashYaml(clashYamlPath = 'Clash3.yaml'):
    import requests
    url = "https://raw.githubusercontents.com/yu-steven/openit/main/Clash.yaml" # some subtle difference!
    r = requests.get(url)
    with open(clashYamlPath, 'w+') as f:
        f.write(r.text)
    print("FETCHING CLASH YAML DONE.")
    print("SAVED AT %s" % clashYamlPath)