from test_commons import *
from pyjom.modules.topicGenerator import OnlineTopicGenerator

label, elem =  OnlineTopicGenerator()
orint(label)
for x in elem:
    print("X",x)
    breakpoint()