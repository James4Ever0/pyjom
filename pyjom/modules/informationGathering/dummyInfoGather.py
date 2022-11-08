from reloading import reloading
from pyjom.commons import *


@decorator
@reloading
def dummyInfo(topic):
    return ["husky", "cats", "kitten"]
