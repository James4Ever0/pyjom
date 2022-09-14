from test_commons import *
from pyjom.modules.topicGenerator import OnlineTopicGenerator

label, elem =  OnlineTopicGenerator()
sprint(label)
breakpoint()
for x in elem:
    print("X",x)
    breakpoint()