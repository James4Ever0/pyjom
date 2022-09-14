from test_commons import *
from pyjom.modules.topicGenerator import OnlineTopicGenerator
from lazero.utils import sprint
label, elem =  OnlineTopicGenerator()
sprint(label)
breakpoint()

for x in elem:
    print("X",x)
    breakpoint()