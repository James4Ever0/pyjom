from reloading import reloading
from pyjom.commons import *


@decorator
@reloading
def dummyReviewer(content):
    return "fantastic. another good day's work."
