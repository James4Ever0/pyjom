import sys

import tempfile

def customExceptHook():
    print("context preserved! please take action!")
    breakpoint()
    print('')

sys.excepthook=customExceptHook