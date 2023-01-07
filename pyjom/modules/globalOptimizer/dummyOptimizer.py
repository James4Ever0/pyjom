from pyjom.commons import *
from lazero.program.functools import (
    iterateWithTempDirectory,
)  # you can also switch to 'AUTO'


@decorator  # called 'iterateWithTempDirectory'
def dummyOptimizer(topic, feedback):  # wtf is this?
    # not optimized. need schedule.
    @iterateWithTempDirectory()
    def inner(elem):
        print("current topic: %s" % str(topic))
        print("from feedback:", elem)
        return "pending"

    return inner(feedback)


@decorator
def dummyReviewOptimizer(topic, feedback, review):
    return "processed and labeled content."
