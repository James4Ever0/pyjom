from pyjom.commons import *
import requests
# import jieba

def topicModeling(, lang='en'): # specify language please?

@decorator
def OnlineTopicGenerator(source='giphy',topic = 'samoyed'):
    if source == 'giphy':
        waitForServerUp(8902, "nodejs giphy server")
        init=True
        while True:
            requests.get("http://localhost:8902/random", params = {})
            requests.get("http://localhost:8902/related", params = {})
            if init: init=False