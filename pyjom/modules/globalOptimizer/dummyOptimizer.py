from pyjom.commons import *


@decorator # called 'iterate with 
def dummyOptimizer(topic, feedback, iterate=False): # wtf is this?
    # not optimized. need schedule.
    if not iterate:
        feedback = [feedback] # feedback is the go. it must be iterable.
    for elem in feedback:
        print("from feedback:", elem)
    return "pending"


@decorator
def dummyReviewOptimizer(topic, feedback, review):
    return "processed and labeled content."
