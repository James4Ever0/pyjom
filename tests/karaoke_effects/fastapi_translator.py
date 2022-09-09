import os

clash_http_port = 8381
os.environ['http_proxy'] = "http://127.0.0.1:{}".format(clash_http_port)
os.environ['https_proxy'] = "http://127.0.0.1:{}".format(clash_http_port)

from fastapi import FastAPI

app = FastAPI()

import time

# you want to wait? or you want to swap?

import paddlehub as hub
language_translation_model = hub.Module(name='baidu_translate')
language_recognition_model = hub.Module(name='baidu_language_recognition')

def baiduTranslator(text): # target language must be chinese.
    try:
        language_code = language_recognition_model.recognize(text)
        if language_code != 'zh':
            text_prompts = language_translation_model.translate(text, language_code, 'zh')
            translatedText =  text_prompts
        else:
            translatedText =  text
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
    code = response['code']
    if code == 200:
        translatedText =  response['data']
        return translatedText
    else:
        print("DEEPL RESPONSE ERROR. PLEASE CHECK")
        print(response)
        # breakpoint()
        return None

def metaTranslator(test, backend='baidu'):
    assert backend in ['baidu','deepl']
    if backend == 'baidu':
        translator = baiduTranslator
    elif backend == 'deepl':
        translator = deeplTranslator
@app.get("/")
def read_root():
    return "unified translator hooked on some clash server"

@app.get("/translate")
def read_item(backend: str, text: str):
    code = 200
    if not backend in ['deepl','baidu']:
        code = 400
        result = 'INVALID BACKEND'
    elif backend == 'deepl':
        result = 
    elif backend == 'baidu':
        result = 
    return {"code":code, "result": result}