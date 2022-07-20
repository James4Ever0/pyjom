from pyjom.commons import *


@decorator
def dummyUpdator(optimized_result):
    return "updated. since it is pending we will schedule another optimization"
