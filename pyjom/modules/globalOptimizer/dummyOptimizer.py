from reloading import reloading
from pyjom.commons import *
from lazero.program.functools import (
    iterateWithTempDirectory,
)  # you can also switch to 'AUTO'


@decorator  # called 'iterateWithTempDirectory'
@reloading
def dummyOptimizer(topic, feedback):  # wtf is this?
    # not optimized. need schedule.
    @iterateWithTempDirectory()
    def inner(elem):
        print("current topic: %s" % topic)
        print("from feedback:", elem)
        return "pending"

    return inner(feedback)


@decorator
@reloading
def dummyReviewOptimizer(topic, feedback, review):
    return "processed and labeled content."
