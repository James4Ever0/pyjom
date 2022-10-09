from pyjom.commons import *


@decorator
def dummyOptimizer(topic, feedback, iterate=False): # wtf is this?
    # not optimized. need schedule.
    if not iterate:
        feedback = [feedback] # feedback is the go. it must be iterable.
    for elem in content:
        print("from poster:", elem)
    return "pending"


@decorator
def dummyReviewOptimizer(topic, feedback, review):
    return "processed and labeled content."
