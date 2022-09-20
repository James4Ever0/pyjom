from lazero.network import waitForServerUp

port = 8576
message = 'progressbar server'
waitForServerUp(port=port, message=message)

import requests

for _ in range()