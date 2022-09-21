from pyjom.commons import *
from pyjom.languagetoolbox import englishTopicModeling
from lazero.utils.tools import flattenUnhashableList # one of my classic methods
import requests

# import jieba
from typing import Literal

def removeKeywordDuplicates(keywords):
    keywordsType = type(keywords)
    inputFuncs = {str: lambda x: x.split(" "), list: lambda x: x, tuple: lambda x: list(x)}
    outputFuncs = {str: lambda x: " ".join(x), list: lambda x: x, tuple: lambda x: tuple(x)}
    if keywordsType in inputFuncs.keys():
        keywordsList = inputFuncs[keywordsType](keywords)
    else:
        raise Exception("Unknown keywords type: %s" % type(keywords))
    keywordsSet = set(keywordsList)
    keywordsSetList = list(keywordsSet)
    return outputFuncs[keywordsType](keywordsSetList)


def topicModeling(sentences: list[str], lang="en"):  # specify language please?
    # python does not enforce type checking. use third party tool such as linter instead.
    if lang == "en":
        topics = englishTopicModeling(sentences)
        return topics


def topicWordSelection(
    topics,
    core_topic_set: set,
    selected_topic_list: list,
    mode: Literal["combined", "separate"] = "combined",
    threshold=10,
):
    if len(selected_topic_list) > threshold:
        for _ in range(len(selected_topic_list) - threshold):
            selected_topic_list.pop(0)  # right way to remove elem from original list.
    selected_topic_set = set(list(core_topic_set) + selected_topic_list)
    import random

    mTopics = topics.copy()
    random.shuffle(mTopics)
    for topic in mTopics:
        words = topic[mode]
        words = [x for x in words if x not in selected_topic_set]
        if len(words) > 0:
            word = random.choice(words)
            selected_topic_list.append(word)  # no need to go elsewhere.
            return word
    print("no topic word this time")
    return None


def getMetaTopicString(metaTopic):
    staticCandidates = [random.choice(x) for x in metaTopic["static"]]
    dynamicCandidates = [random.choice(x) for x in metaTopic["dynamic"]]
    samples = random.sample(
        dynamicCandidates, random.randint(0, len(dynamicCandidates))
    )
    return " ".join(staticCandidates + samples)


@decorator
def OnlineTopicGenerator(
    source="giphy",
    metaTopic={
        "static": [["dog", "cat"], ["funny", "cute"]],
        "dynamic": [["samoyed", "husky", "teddy", "chiwawa"]],
    },  # this is not a matrix.
    # sample_size = 10 # per search.
):
    getKeywords = lambda: getMetaTopicString(metaTopic)
    core_topic_set = {
        *flattenUnhashableList(metaTopic)
    }  # common way to initialize a set.
    selected_topic_list = []
    if source == "giphy":
        waitForServerUp(8902, "nodejs giphy server")
        keywords = getKeywords()
        while True:
            harvestedData = []
            try:
                source_type = random.choice(["videos", "gifs"])
                # source_type = 'videos' # for debugging
                if random.random() > 0.5:
                    with requests.get(
                        "http://127.0.0.1:8902/random",
                        params={"q": keywords, "rating": "g", "type": source_type},
                    ) as mRandomPicture: # may you get stickers?
                        mRandomPictureJson = mRandomPicture.json()
                        harvestedData += mRandomPictureJson["data"]
                        randomPictureId = mRandomPictureJson["data"][0]["id"]
                else:
                    with requests.get(
                        "http://127.0.0.1:8902/search",
                        params={"q": keywords, "rating": "g", "type": source_type},
                    ) as mSearchPictures:
                        mSearchPicturesJson = mSearchPictures.json()
                        harvestedData += mSearchPicturesJson["data"]
                        randomPictureId = random.choice(mSearchPicturesJson["data"])["id"]

                with requests.get(
                    "http://127.0.0.1:8902/related",
                    params={
                        "q": randomPictureId,
                        "type": source_type,
                    },  # seems not working? wtf?
                ) as mRelatedPictures:
                    mRelatedPicturesJson = mRelatedPictures.json()
                harvestedData += mRelatedPicturesJson["data"]
                sentences = [x["title"] for x in mRelatedPicturesJson["data"]]
                topics = topicModeling(sentences)
                selectedWord = topicWordSelection(
                    topics, core_topic_set, selected_topic_list
                )
                if not selectedWord is None:
                    keywords = " ".join(
                        [getKeywords(), selectedWord]
                    )  # for next iteration.
                    print("REFRESHING KEYWORDS:", keywords)
                else:
                    keywords = getKeywords()
                # recheck keywords!
                keywords = removeKeywordDuplicates(keywords)
            except:
                import traceback
                traceback.print_exc()
                print("ERROR WHEN FETCHING GIPHY TOPIC")
            for elem in harvestedData:
                yield elem["id"], json_auto_float_int(elem["media"])
