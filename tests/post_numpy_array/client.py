import numpy as np
import requests
import numpy_serializer

# this is pure magic. shit.

from server import SERVER_PORT
image = np.array([1,2,3])
image_bytes = numpy_serializer.to_bytes(image)
data = {'image':image_bytes}
print("BYTES?", image_bytes)
r = requests.post("http://localhost:{}".format(SERVER_PORT),data=data,params={'isBytes':True,'debug':True})
print('RESPONSE?',r.text)

def docstring(): # malformat
    import textwrap
    a ="""
    lmn
    abcdefg 
    hijk
    """
    print(a)
    print()
    print(textwrap.dedent(a))
    # inspect.cleandoc
    # https://9to5answer.com/how-to-remove-extra-indentation-of-python-triple-quoted-multi-line-strings

docstring()