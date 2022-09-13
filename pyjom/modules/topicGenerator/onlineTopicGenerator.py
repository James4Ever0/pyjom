from pyjom.commons import *
import requests

@decorator
def OnlineTopicGenerator(source='giphy',topic = 'samoyed'):
    if source == 'giphy':
        waitForServerUp(8902, "nodejs giphy server")
        requests.get("http://localhost:8902/random")