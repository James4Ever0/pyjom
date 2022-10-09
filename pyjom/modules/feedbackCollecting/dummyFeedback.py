from pyjom.commons import *


@decorator
def dummyFeedback(
    content, iterate=False
):  # anyway, it is dummy. i don't expect nothing.
    def inner()
    if not iterate:
        content = [content]
    for elem in content:
        
