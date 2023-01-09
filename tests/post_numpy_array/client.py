import numpy as np
import requests
import numpy_serializer as ns
from server import SERVER_PORT
image = np.array([1,2,3])
image_bytes = ns.to_bytes(image)
data = {'images':image_bytes}
print("BYTES?", image_bytes)
r = requests.post("http://localhost:{}".format(SERVER_PORT),data=data,params={'isBytes':True})
print('RESPONSE?',r.text)