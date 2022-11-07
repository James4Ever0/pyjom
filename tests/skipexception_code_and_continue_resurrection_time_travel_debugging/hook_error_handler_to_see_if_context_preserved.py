import sys

import tempfile

def customExceptHook():
    print("context preserved! please take action!")
    while True:
        input('exit? (y for exit)\n')
    print('closing program now!')

sys.excepthook=customExceptHook