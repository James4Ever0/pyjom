from typing import Union

from fastapi import FastAPI

app = FastAPI()

import paddlehub as hub
language_translation_model = hub.Module(name='baidu_translate')
language_recognition_model = hub.Module(name='baidu_language_recognition')

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