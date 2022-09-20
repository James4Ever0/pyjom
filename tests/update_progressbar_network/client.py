from lazero.network import waitForServerUp

port = 8576
message = 'progressbar server'
waitForServerUp(port=port, message=message)

import requests

requests.get('http://localhost:8576',proxies=None,)
for _ in range(200):