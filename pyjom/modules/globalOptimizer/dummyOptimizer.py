from pyjom.commons import *
from lazero.program.functools import iterateWithTempDirectory

@decorator # called 'iterateWithTempDirectory'
def dummyOptimizer(topic, feedback, iterate=False): # wtf is this?
    # not optimized. need schedule.
    @iterateWithTempDirectory(topic
    def inner(elem):
        print("from feedback:", elem)
    return "pending"


@decorator
def dummyReviewOptimizer(topic, feedback, review):
    return "processed and labeled content."
