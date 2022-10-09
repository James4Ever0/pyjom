from pyjom.commons import *


@decorator
def dummyFeedback(
    content, iterate=False
):  # anyway, it is dummy. i don't expect nothing.
    def inner(elem):
        print("from poster:", elem)
        return "pending"
    def innerIterator(content):
        for elem in content:
            yield inner(elem)
    if not iterate:
        return inner(content)
    else:
        return innerIterator(content)
        
