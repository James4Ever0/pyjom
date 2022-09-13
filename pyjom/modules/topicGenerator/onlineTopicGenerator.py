from pyjom.commons import *
import requests
# import jieba

def topicModeling(sentences: list[str], lang='en'): # specify language please?
    # python does not enforce type checking. use third party tool such as linter instead.
    if lang == 'en':
        from gensim.parsing.preprocessing import remove_stopwords
result = remove_stopwords("""He determined to drop his litigation with the monastry, and relinguish his claims to the 
wood-cuting and fishery rihgts at once. He was the more ready to do this becuase the rights had become much less valuable, 
and he had indeed the vaguest idea where the wood and river in question were.""")

@decorator
def OnlineTopicGenerator(source='giphy',topic = 'samoyed'):
    if source == 'giphy':
        waitForServerUp(8902, "nodejs giphy server")
        init=True
        while True:
            mRandomPicture = requests.get("http://localhost:8902/random", params = {'q':keywords, 'rating':'g'}) # may you get stickers?
            mRelatedPictures = requests.get("http://localhost:8902/related", params = {'q':randomPictureId, })
            if init: init=False