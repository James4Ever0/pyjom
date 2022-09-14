from test_commons import *
from pyjom.modules.topicGenerator import OnlineTopicGenerator
from lazero.utils import sprint

elem, label = OnlineTopicGenerator()
sprint("LABEL:",label)
# # 'pyjom.commons.OnlineTopicGenerator'
# breakpoint()

for x in elem:
    print("X",x)
    # X ('sr8jYZVVsCmxddga8w', {'height': 480, 'width': 474, 'url': 'https://media0.giphy.com/media/sr8jYZVVsCmxddga8w/giphy.gif'})
    breakpoint()