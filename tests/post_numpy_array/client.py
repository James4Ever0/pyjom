import numpy as np
import requests
import numpy_serializer as ns
from server import SERVER_PORT
image = np.array([1,2,3])
image_bytes = ns.to_bytes(image)
data = {'image':image_bytes}
r = requests.post("http://localhost:{}".format(SERVER_PORT),data=data)
print('RESPONSE?',r.text)