SERVER_PORT = 9341

if __name__ == "__main__":
    from fastapi import FastAPI
    app = FastAPI()
    import time

    @app.get("/")
    def receiveImage():
        time.sleep(10)
        return "hello world"
    
    import uvicorn
    # checking: https://9to5answer.com/python-how-to-use-fastapi-and-uvicorn-run-without-blocking-the-thread

    def run(host='0.0.0.0',port=SERVER_PORT): 
        """
        This function to run configured uvicorn server.
        """
        uvicorn.run(app=app, host=host, port=port)
    run()