from pyjom.commons import *


@decorator
def dummyFeedback(content, iterate=False): # anyway, it is dummy. i don't expect nothing.
    if not iterate:
        
        for elem in content:
            print('from poster:', elem)
    return "pending"
