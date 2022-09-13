from pyjom.commons import *
import requests

@decorator
def OnlineTopicGenerator(source='giphy',topic = 'samoyed'):
    requests.get("")