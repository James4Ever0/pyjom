import sys

import tempfile

def customExceptHook():
    print("context preserved! please take action!")
    breakpoint()

sys.excepthook=customExceptHook