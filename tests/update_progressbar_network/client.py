import requests

class netProgressbar:
    def __init__(self, port = 8576, message = 'progressbar server'):
        from lazero.network import waitForServerUp
        self.port = port
        self.message = message
        waitForServerUp(port=port, message=message)
    def reset(self, total:int):
        requests.get('http://localhost:8576/reset',proxies=None,params = {'total':total})


while True:
    requests.get('http://localhost:8576/reset',proxies=None,params = {'total':200})
    for _ in range(200):
        import time
        time.sleep(0.1)
        requests.get('http://localhost:8576/update',proxies=None)