from test_commons import *
from pyjom.modules.topicGenerator import OnlineTopicGenerator
from lazero.utils import sprint

elem, label = OnlineTopicGenerator()
sprint(label)
# # 'pyjom.commons.OnlineTopicGenerator'
# breakpoint()

for x in elem:
    print("X",x)
    breakpoint()