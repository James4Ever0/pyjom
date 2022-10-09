from pyjom.commons import *


@decorator
def dummyFeedback(content, iterate=False):
    if iterate:
        for _ in content:
            ...
    return "pending"
