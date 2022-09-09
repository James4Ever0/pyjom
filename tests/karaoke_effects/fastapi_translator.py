import os

# before that, we need to fix cv2
import pathlib
import sys

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

import time

# you want to wait? or you want to swap?

import paddlehub as hub

language_translation_model = hub.Module(name="baidu_translate")
language_recognition_model = hub.Module(name="baidu_language_recognition")


def baiduTranslator(text, sleep=1):  # target language must be chinese.
    useProxy(False)
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


def deeplTranslator(text, sleep=2, timeout = 3):
    useProxy(False)
    import requests
    import time
    import filelock

    lock = filelock.FileLock("/root/Desktop/works/pyjom/tests/karaoke_effects/deepl_translator.lock")
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
        proxyName = proxyName['text']
    print("PROXY REFRESHED")
    return proxyName


def metaTranslator(text, backend="baidu"):
    global workingProxies
    assert backend in ["baidu", "deepl"]
    # translator = None
    import random

    getUseDirect = lambda: False
    if backend == "baidu":
        translator = baiduTranslator
        getUseDirect = lambda: True
        # let's just bet on this shit.
        # getUseDirect = lambda: random.random() > 0.7
    elif backend == "deepl":
        translator = deeplTranslator
    proxyName = None
    firstTime = True
    while True:
        try:
            if not firstTime:
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


@app.get("/")
def read_root():
    return "unified translator hooked on some clash server"


@app.get("/translate")
def read_item(backend: str, text: str):
    code = 200
    if not backend in ["deepl", "baidu"]:
        code = 400
        result = "INVALID BACKEND"
    else:
        result = metaTranslator(text, backend=backend)
    return {"code": code, "result": result}
