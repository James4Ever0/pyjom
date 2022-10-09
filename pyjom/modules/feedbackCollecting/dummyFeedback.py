from pyjom.commons import *


@decorator
def dummyFeedback(
    content, iterate=False
):  # anyway, it is dummy. i don't expect nothing.
    def inner(elem):
        print("from poster:", elem)
        return "pending"
    if not iterate:
        return inner()
    for elem in content:
        
