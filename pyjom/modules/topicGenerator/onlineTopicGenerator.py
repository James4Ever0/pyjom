from pyjom.commons import *
import requests

@decorator
def OnlineTopicGenerator(source='giphy',topic = 'samoyed'):
    if source == 'giphy':
        waitForServerUp(8902, "")
        requests.get("")