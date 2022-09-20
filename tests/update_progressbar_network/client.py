import requests

class netProgressbar:
    def __init__(self, port = 8576, message = 'progressbar server'):
        from lazero.network import waitForServerUp
        self.port = port
        self.message = message
        waitForServerUp(port=port, message=message)
    def reset(self, total:int):
        requests.get('http://localhost:{}/reset'.format(self.port),proxies=None,params = {'total':total})
    def update(self,progress:int=1):
        requests.get('http://localhost:8576/update',proxies=None, params={'progress':progress})