from pyjom.commons import *
from lazero.program.functools import 

@decorator # called 'iterateWithTempDirectory'
def dummyOptimizer(topic, feedback, iterate=False): # wtf is this?
    # not optimized. need schedule.

    def inner(elem):
        print("from feedback:", elem)
    return "pending"


@decorator
def dummyReviewOptimizer(topic, feedback, review):
    return "processed and labeled content."
