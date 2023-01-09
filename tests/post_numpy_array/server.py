
SERVER_PORT=5463

if __name__ == '__main__':
    # from pydantic import BaseModel
    # import numpy as np
    import numpy_serializer
    # from typing import Union
    # class Image(BaseModel):
    #     image:Union[str,bytes]

    from fastapi import FastAPI, Body

    app = FastAPI()

    @app.post("/")
    def receiveImage(image:bytes=Body(default=None),
        isBytes:bool =False,
    encoding:str='utf-8', debug:bool=False):
        # return book
        # print('image type:',type(image))
        # print(image)
        import urllib.parse
        image = image.removeprefix(b'image=') # fuck man.
        image = urllib.parse.unquote_to_bytes(image)
        if debug:
            print("isBytes:",isBytes)
        if not isBytes:
            image = image.decode(encoding) #fuck?
            # read image from path, url
        else:
            image = numpy_serializer.from_bytes(image)
        if debug:
            print('shape?',image.shape)
            print('image?',image)
        return "good"

    import uvicorn
    # checking: https://9to5answer.com/python-how-to-use-fastapi-and-uvicorn-run-without-blocking-the-thread

    def run(host='0.0.0.0',port=SERVER_PORT): 
        """
        This function to run configured uvicorn server.
        """
        uvicorn.run(app=app, host=host, port=port)
    run()