import numpy as np
import requests
import numpy_serializer as ns

# this is pure magic. shit.

from server import SERVER_PORT
image = np.array([1,2,3])
image_bytes = ns.to_bytes(image)
data = {'image':image_bytes}
print("BYTES?", image_bytes)
r = requests.post("http://localhost:{}".format(SERVER_PORT),data=data,params={'isBytes':True,'debug':True})
print('RESPONSE?',r.text)

def docstring(): # malformat
    a ="""
    lmn
    abcdefg 
    hijk
    """
    print(a)

docstring()