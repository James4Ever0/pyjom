from pyjom.commons import *
from lazero.program.functools import iterateWithTempDirectory

@decorator # called 'iterateWithTempDirectory'
def dummyOptimizer(topic, feedback, iterate=False): # wtf is this?
    # not optimized. need schedule.
    @iterateWithTempDirectory()
    def inner(elem):
        print("from feedback:", elem)
        return "pending"
    return inner(feedback)


@decorator
def dummyReviewOptimizer(topic, feedback, review):
    return "processed and labeled content."
