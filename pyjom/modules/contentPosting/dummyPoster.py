from pyjom.commons import *

@decorator
def dummyPoster(content, iterate=False):
    if iterate:
        for elem in content:
            print("READY TO POST CONTENT FROM:",elem)
    return "mydarnprotocol://mydarnlink"
