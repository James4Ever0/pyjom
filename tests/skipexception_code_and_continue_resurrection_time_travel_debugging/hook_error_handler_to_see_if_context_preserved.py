import sys

import tempfile

def customExceptHook():
    print("context preserved! please take action!")
    
    print('closing program now!')

sys.excepthook=customExceptHook