from lazero.filesystem.io import readJsonObjectFromFile
from lazero.utils.mathlib import checkMinMaxDict

data = readJsonObjectFromFile("result_baidu.json")
import string
from zhon import hanzi


punctuations = set(list(string.punctuation + hanzi.punctuation))
permitted = [" "]
for perm in permitted:
    if perm in punctuations:
        punctuations.remove(perm)


def removeTimeInfo(phrase):
    import re

    timeinfos = re.findall(r"\d+年\d+月\d+日", phrase)
    for timeinfo in timeinfos:
        phrase = phrase.replace(timeinfo, "")
    return phrase


def processQueryResult(abstract, minMaxDict={"min": 8, "max": 24}):
    for punc in punctuations:
        abstract = abstract.replace(punc, "\n")
    abstract = abstract.split("\n")
    for phrase in abstract:
        phrase = removeTimeInfo(phrase)
        phrase = phrase.strip()
        if not checkMinMaxDict(len(phrase), minMaxDict):
            continue
        else:
            yield phrase


candidates = []

query = "python有个问题想请教一下 为什么我这个函数跑不通"
# use another model please?
# haystack?
for elem in data:
    title = elem.get("title")
    print("title: %s" % title)
    spliters = [" - ", "-", "_", "－"]
    for spliter in spliters:
        title = title.replace(spliter, "_")

    potentialWebsiteNames = title.split("_")
    title = potentialWebsiteNames[0].strip()
    realWebsiteNames = []
    if len(potentialWebsiteNames) > 1:
        websiteNames = potentialWebsiteNames[1:]
        for name in websiteNames:
            name = name.strip()
            if len(name) > 0:
                realWebsiteNames.append(name)
    abstract = elem.get("abstract")
    # print(abstract)
    # breakpoint()
    for name in realWebsiteNames:
        abstract = abstract.replace(name, "")  # remove website names
    for phrase in processQueryResult(abstract):
        if phrase not in candidates and not phrase.endswith(""):  # magic char.
            candidates.append(phrase)  # what is your query?
import jieba


def getCuttedWords(phrase):
    candidates = jieba.lcut(phrase.lower())
    wordList = []
    for word in candidates:
        word = word.strip()
        if len(word) > 0:
            wordList.append(word)
    return wordList


def countCommonWords(phrase_1, phrase_2, wordCount=False):
    words_1 = getCuttedWords(phrase_1)
    words_2 = getCuttedWords(phrase_2)
    # count for longest total length?
    result = list(set(words_1) & set(words_2))
    if wordCount:
        return len(result)
    else:
        return len("".join(result))


# candidates = list(set(candidates))
# https://pypi.org/project/rank-bm25/
# candidates.sort(key=lambda phrase: -countCommonWords(phrase,query))
# use bm25?
# this sorting is wrong.

from rank_bm25 import BM25Okapi

tokenized_corpus = [getCuttedWords(phrase) for phrase in candidates]
tokenized_query = getCuttedWords(query)
bm25 = BM25Okapi(tokenized_corpus)
# doc_scores = bm25.get_scores(tokenized_query)
top_k = 20
print("TOP", top_k)
topKCandidates = bm25.get_top_n(tokenized_query, candidates, n=top_k)
# count chinese chars.
# count for english/chinese portion. (strange hack.)
import numpy as np


def calculateChinesePortion(phrase):
    length = len(phrase)
    mdata = []
    isalpha, isascii, isdigit, ischinese = 0, 0, 0, 0
    for char in phrase:
        isalpha += int(char.isalpha())
        isascii += int(char.isascii())
        isdigit += int(char.isdigit())
        ischinese += int(not (isalpha or isascii or isdigit))
    mdata = np.array([isalpha, isascii, isdigit, ischinese]) / length
    return mdata


queryChinesePortion = calculateChinesePortion(query)
from scipy.spatial.distance import cosine

topKCandidates.sort(
    key=lambda phrase: cosine(calculateChinesePortion(phrase), queryChinesePortion)
)
# topKCandidates.sort(key=lambda phrase: -len(phrase))
for elem in topKCandidates:
    print(elem.__repr__())
