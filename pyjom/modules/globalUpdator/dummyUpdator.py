from pyjom.commons import *
from lazero.program.functools import iterateWithTempDirectory

@decorator
@iterateWithTempDirectory()
def dummyUpdator(optimized_result):
    return "updated. since it is pending we will schedule another optimization"
