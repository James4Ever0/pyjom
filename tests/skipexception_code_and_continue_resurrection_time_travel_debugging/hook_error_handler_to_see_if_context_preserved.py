import sys

import tempfile

def customExceptHook():
    print("context preserved! please take action!")
    

sys.excepthook=customExceptHook