from pyjom.commons import *


@decorator
def dummyFeedback(content, iterate=False): # anyway, it is dummy. i don't expect nothing.
    if iterate:
        for elem in content:
            ...
    return "pending"
