from test_commons import *
from pyjom.modules.topicGenerator import OnlineTopicGenerator

label, elem =  OnlineTopicGenerator():
    # print(elem) # a generator in generator?
    # breakpoint()
    for x in elem:
        print("X",x)
        breakpoint()