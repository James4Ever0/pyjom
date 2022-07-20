# from typing import Union

# from fastapi import FastAPI

# app = FastAPI()


# @app.get("/")
# def read_root():
#     return {"Hello": "World"}


# @app.get("/chat")
# def read_item(text: Union[str, None] = None):
#     return {"q": text}

from flask import Flask, request
app = Flask(__name__)

@app.route('/',methods= ['GET'])
def hello_world():
    args = request.args
    print(type(args), args)
    breakpoint()
    return 'abc'

if __name__ == "__main__":
    app.run(port=8987)