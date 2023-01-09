
SERVER_PORT=5463

if __name__ == '__main__':
    from pydantic import BaseModel
    # import numpy as np
    import numpy_serializer as ns
    from typing import Union
    class Image(BaseModel):
        image:Union[str,bytes]

    from fastapi import FastAPI

    app = FastAPI()

    @app.post("/")
    def create_book(image:Union[str,bytes]):
        # return book
        image = ns.from_bytes(image)
        print(image.shape)
        return "good"


    import uvicorn
    # checking: https://9to5answer.com/python-how-to-use-fastapi-and-uvicorn-run-without-blocking-the-thread

    def run(host='0.0.0.0',port=SERVER_PORT): 
        """
        This function to run configured uvicorn server.
        """
        uvicorn.run(app=app, host=host, port=port)
    run()