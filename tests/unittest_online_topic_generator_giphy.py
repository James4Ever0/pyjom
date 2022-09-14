from test_commons import *
from pyjom.modules.topicGenerator import OnlineTopicGenerator

for elem in OnlineTopicGenerator():
    # print(elem) # a generator in generator?
    # breakpoint()
    for x in elem:
        print(x)
        breakpoint()