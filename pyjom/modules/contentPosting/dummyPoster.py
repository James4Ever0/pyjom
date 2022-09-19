from pyjom.commons import *


@decorator
def dummyPoster(content, iterate=True):
    if iterate:
        for elem in content:
            print(elem)
    return "mydarnprotocol://mydarnlink"
