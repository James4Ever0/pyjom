from pyjom.commons import *


@decorator
def dummyOptimizer(topic, feedback):
    # not optimized. need schedule.
    return "pending"


@decorator
def dummyReviewOptimizer(topic, feedback, review):
    return "processed and labeled content."
