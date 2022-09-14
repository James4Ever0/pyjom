from pyjom.commons import *
from pyjom.languagetoolbox import englishTopicModeling
import requests
# import jieba

def topicModeling(sentences: list[str], lang='en'): # specify language please?
    # python does not enforce type checking. use third party tool such as linter instead.
    if lang == 'en':
        topics = englishTopicModeling(sentences)

@decorator
def OnlineTopicGenerator(source='giphy',topic = 'samoyed'):
    if source == 'giphy':
        waitForServerUp(8902, "nodejs giphy server")
        init=True
        while True:
            mRandomPicture = requests.get("http://localhost:8902/random", params = {'q':keywords, 'rating':'g'}) # may you get stickers?
            mRelatedPictures = requests.get("http://localhost:8902/related", params = {'q':randomPictureId, })
            if init: init=False