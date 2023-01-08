import os

# before that, we need to fix cv2
import pathlib
import sys

from isort import stream

site_path = pathlib.Path("/usr/local/lib/python3.9/site-packages")
cv2_libs_dir = (
    site_path / "cv2" / f"python-{sys.version_info.major}.{sys.version_info.minor}"
)
print(cv2_libs_dir)
cv2_libs = sorted(cv2_libs_dir.glob("*.so"))
if len(cv2_libs) == 1:
    print("INSERTING:", cv2_libs[0].parent)
    sys.path.insert(1, str(cv2_libs[0].parent))

clash_http_port = 8381
# wtf is wrong with this shit?
def useProxy(flag):
    if flag:
        os.environ["http_proxy"] = "http://127.0.0.1:{}".format(clash_http_port)
        os.environ["https_proxy"] = "http://127.0.0.1:{}".format(clash_http_port)
    else:
        os.environ["http_proxy"] = ""
        os.environ["https_proxy"] = ""


from fastapi import FastAPI

app = FastAPI()

# import time

# you want to wait? or you want to swap?

import paddlehub as hub

language_translation_model = hub.Module(name="baidu_translate")
language_recognition_model = hub.Module(name="baidu_language_recognition")


def baiduTranslator(text, sleep=1):  # target language must be chinese.
    useProxy(False)
    import filelock

    lock = filelock.FileLock(
        "/root/Desktop/works/pyjom/tests/karaoke_effects/baidu_translator.lock"
    )
    with lock:
        import time

        time.sleep(sleep)
        try:
            language_code = language_recognition_model.recognize(text)
            if language_code != "zh":
                text_prompts = language_translation_model.translate(
                    text, language_code, "zh"
                )
                translatedText = text_prompts
            else:
                translatedText = text
            return translatedText
        except:
            import traceback

            traceback.print_exc()
            print("ERROR ON BAIDU TRANSLATOR")
            return None


from lazero.network.proxy.clash import (
    getTestedProxyList,
    setProxyWithSelector,
    clashProxyStateManager,
)

proxyList = []
refreshProxyCounter = 0


def deeplTranslator(text, sleep=2, timeout=5, mod=40):
    global proxyList, refreshProxyCounter
    useProxy(False)
    import random

    if (
        refreshProxyCounter % mod == 0
    ):  # make sure it will be launched at the first request.
        proxyList = getTestedProxyList()
        refreshProxyCounter %= mod
    refreshProxyCounter += 1
    proxyName = random.choice([proxy["name"] for proxy in proxyList] + ["DIRECT"])
    setProxyWithSelector(proxyName)
    # better use proxy instead. you need to config it here, and make sure the deepl adaptor uses the proxy.
    import requests
    import time
    import filelock

    lock = filelock.FileLock(
        "/root/Desktop/works/pyjom/tests/karaoke_effects/deepl_translator.lock"
    )
    with clashProxyStateManager("Global", "Rule"):
        with lock:
            time.sleep(sleep)
            port = 8281
            # env ROCKET_PORT=8281 ./executable_deepl
            url = "http://127.0.0.1:{}/translate".format(port)
            data = {"text": text, "source_lang": "auto", "target_lang": "ZH"}
            r = requests.post(url, json=data, timeout=timeout)
            response = r.json()
            code = response["code"]
            if code == 200:
                translatedText = response["data"]
                return translatedText
            else:
                print("DEEPL RESPONSE ERROR. PLEASE CHECK")
                print(response)
                proxyList = getTestedProxyList()
                refreshProxyCounter = 1
                # breakpoint()
                return None


# use suggest mechanism
workingProxies = set()


def checkWorkingProxies():
    global workingProxies
    useProxy(False)
    url = "http://127.0.0.1:8677/checkProxy"
    import requests

    for proxy in list(workingProxies):
        # proxy could be None.
        # print([proxy])
        # breakpoint()
        r = requests.get(url, params={"proxy": proxy})
        response = r.json()
        if not response["exists"]:
            print("REMOVING PROXY %s NOW" % useProxy)
            workingProxies.remove(proxy)


def changeProxy(useDirect=False, suggestSingleElemProbability=0.1):
    useProxy(False)
    global workingProxies
    checkWorkingProxies()
    import requests

    if useDirect:
        path = "useDirect"
    else:
        path = "refreshProxy"
    print("PATH", path)
    if path == "refreshProxy":
        import random

        prob = random.random() < len(workingProxies) * suggestSingleElemProbability
        if prob:
            suggestedProxy = random.choice(list(workingProxies))
            params = {"suggest": suggestedProxy}
            print("SUGGESGING PROXY:", suggestedProxy)
        else:
            params = {}
            # params = {"suggest": None}
        r = requests.get("http://127.0.0.1:8677/{}".format(path), params=params)
    else:
        r = requests.get("http://127.0.0.1:8677/{}".format(path))
    print("RESPONSE:", r.text)
    import parse

    proxyName = parse.parse("refresh proxy to {text}", r.text)
    if proxyName == None:
        # using suggested proxy here.
        print("USING SUGGESTED PROXY")
    else:
        proxyName = proxyName["text"]
    print("PROXY REFRESHED")
    return proxyName


def metaTranslator(text, backend="baidu", max_tries: int = 3):
    global workingProxies
    backendList = ["baidu", "deepl"]
    assert backend in backendList
    # translator = None
    import random

    getUseDirect = lambda: False
    backends = {
        "baidu": (baiduTranslator, lambda: True),
        # "deepl": (deeplTranslator, lambda: False), # use direct? no proxy?
        "deepl": (
            deeplTranslator,
            lambda: True,
        ),  # the proxy is used by deepl client, not here!
    }
    translator, getUseDirect = backends[backend]
    proxyName = None
    firstTime = True
    for _ in range(max_tries):
        try:
            if not firstTime:  # after first 'failed' trial we will change the strategy.
                key = random.choice(backendList)
                translator, getUseDirect = backends[key]
                proxyName = changeProxy(useDirect=getUseDirect())
            else:
                firstTime = False
            result = translator(text)
            if result:
                if proxyName:
                    workingProxies.add(proxyName)
                return result
            else:
                if proxyName in workingProxies:
                    workingProxies.remove(proxyName)
                print("SOME ERROR DURING FETCHING TRANSLATION")
        except:
            import traceback

            traceback.print_exc()
            print("ERROR FETCHING TRANSLATION")


# def waitForServerUp(port, message, timeout=1):
#     import requests

#     while True:
#         try:
#             url = "http://localhost:{}".format(port)
#             r = requests.get(url, timeout=timeout)
#             text = r.text.strip('"').strip("'")
#             print("SERVER AT PORT %d RESPONDS:" % port, [text])
#             assert text == message
#             print("SERVER AT PORT %d IS UP" % port)
#             break
#         except:
#             import traceback

#             traceback.print_exc()
#             print("SERVER AT PORT %d MIGHT NOT BE UP")
#             print("EXPECTED MESSAGE:", [message])
#             import time

#             time.sleep(1)


@app.get("/")
def read_root():
    # waitForServerUp(8677, "clash update controller")  # probe the clash updator
    return "unified translator hooked on some clash server"


translatedDict = {}

translatedDictCacheLimit = 100


@app.get("/translate")
def read_item(backend: str, text: str):
    global translatedDict
    if len(list(translatedDict.keys())) > translatedDictCacheLimit:
        mkeys = list(translatedDict.keys())
        import random

        random.shuffle(mkeys)
        for key in mkeys[:translatedDictCacheLimit]:
            del translatedDict[key]
    code = 200
    if not backend in ["deepl", "baidu"]:
        code = 400
        result = "INVALID BACKEND"
    else:
        if len(text) < 30 and text in translatedDict.keys():
            result = translatedDict[text]
        else:
            result = metaTranslator(text, backend=backend)
            if type(result) == str:
                if len(result) < 30 and len(text) < 30:
                    translatedDict.update({text: result})
    return {
        "code": (code if result not in [None, False, True, ""] else 400),
        "result": (result if type(result) == str and result != "" else None),
    }
