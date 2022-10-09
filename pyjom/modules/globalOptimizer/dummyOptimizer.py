from pyjom.commons import *


@decorator
def dummyOptimizer(topic, feedback, iterate=False):
    # not optimized. need schedule.
    if not iterate:
        content = [content]
    for elem in content:
        print("from poster:", elem)
    return "pending"


@decorator
def dummyReviewOptimizer(topic, feedback, review):
    return "processed and labeled content."
