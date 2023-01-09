import numpy as np
import requests

from server import SERVER_PORT
image = np.array([1,2,3])
data = {'image':image}
r = requests.post("http://localhost:{}".format(SERVER_PORT),data=data)
print('RESPONSE?',r.text)