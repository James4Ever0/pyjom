import sys

import tempfile

def customExceptHook(a,b,c):
    print("context preserved! please take action!")
    while True:
        i = input('exit? (y for exit)\n').lower()
        if i == 'y':
            break
    print('closing program now!')

sys.excepthook=customExceptHook

with tempfile.NamedTemporaryFile(suffix='123',dir=".") as f:
    maketrouble()