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
os.environ["http_proxy"] = "http://127.0.0.1:{}".format(clash_http_port)
os.environ["https_proxy"] = "http://127.0.0.1:{}".format(clash_http_port)

from fastapi import FastAPI

app = FastAPI()

import time

# you want to wait? or you want to swap?

import paddlehub as hub

language_translation_model = hub.Module(name="baidu_translate")
language_recognition_model = hub.Module(name="baidu_language_recognition")


def baiduTranslator(text):  # target language must be chinese.
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


def deeplTranslator(text):
    import requests

    port = 8281
    # env ROCKET_PORT=8281 ./executable_deepl
    url = "http://localhost:{}/translate".format(port)
    data = {"text": text, "source_lang": "auto", "target_lang": "ZH"}
    r = requests.post(url, json=data)
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


def changeProxy(useDirect=False):
    import requests

    if useDirect:
        path = "useDirect"
    else:
        path = "refreshProxy"
    r = requests.get("http://localhost:8677/{}".format(path))
    print("RESPONSE:", r.text)
    print("PROXY REFRESHED")


def metaTranslator(text, backend="baidu"):
    assert backend in ["baidu", "deepl"]
    # translator = None
    import random

    getUseDirect = lambda: False
    if backend == "baidu":
        translator = baiduTranslator
        getUseDirect = lambda: random.random() > 0.7
    elif backend == "deepl":
        translator = deeplTranslator
    while True:
        try:
            changeProxy(useDirect=getUseDirect())
            result = translator(text)
            if result:
                return result
            else:
                print("SOME ERROR DURING FETCHING TRANSLATION")
        except:
            import traceback
            traceback.print_exc()
            print('ERROR FETCHING TRANSLATION')


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
