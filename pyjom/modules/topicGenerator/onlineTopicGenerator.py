from pyjom.commons import *
import requests

@decorator
def OnlineTopicGenerator(source='giphy',topic = 'samoyed'):
    if source == 'giphy':
        requests.get("")