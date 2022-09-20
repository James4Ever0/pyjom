from lazero.network import waitForServerUp

port = 8576
message = 'progressbar server'
waitForServerUp(port=port, message=message)

import requests

while True:
    requests.get('http://localhost:8576/reset',proxies=None,params = {'total':200})
    for _ in range(200):
        requests.get('http://localhost:8576/update',proxies=None)