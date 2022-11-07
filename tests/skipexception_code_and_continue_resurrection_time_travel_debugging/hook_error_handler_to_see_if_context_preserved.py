import sys

import tempfile

def customExceptHook(a,b,c):
    print('ERROR INFO:', a,b,c)
    # <class 'AttributeError'> '_io.BufferedRandom' object has no attribute 'path' <traceback object at 0x7fd6c4325080>
    # it is a traceback object.
    print("context preserved! please take action!")
    while True:
        i = input('exit? (y for exit)\n').lower()
        if i == 'y':
            break
    print('closing program now!')

sys.excepthook=customExceptHook
import os
with tempfile.NamedTemporaryFile(suffix='123') as f:
    # print('LOCATION:',dir(f))
    # /tmp/tmp7c5ffugz123 
    print('LOCATION:',os.path.abspath(f.name))
    maketrouble()