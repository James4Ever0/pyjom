from pyjom.commons import *
import requests


def topicModeling():

@decorator
def OnlineTopicGenerator(source='giphy',topic = 'samoyed'):
    if source == 'giphy':
        waitForServerUp(8902, "nodejs giphy server")

            requests.get("http://localhost:8902/random", params = {})
            requests.get("http://localhost:8902/related", params = {})