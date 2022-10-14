from lazero.filesystem.io import readJsonObjectFromFile
from lazero.utils.mathlib import checkMinMaxDict
data = readJsonObjectFromFile('result_baidu.json')
import string
from zhon import hanzi


punctuations = set(list(string.punctuation+hanzi.punctuation))
permitted = [" "]
for perm in permitted:
    if perm in punctuations:
        punctuations.remove(perm)
    

def removeTimeInfo(phrase):
    import re
    timeinfos = re.findall(r'\d+年\d+月\d+日', phrase)
    for timeinfo in timeinfos:
        phrase = phrase.replace(timeinfo, "")
    return phrase
def processQueryResult(abstract, minMaxDict={'min':5,'max':24}):
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
import Levenshtein

query = "python有个问题想请教一下 为什么我这个函数跑不通"
# use another model please?
# haystack?
for elem in data:
    title = elem.get('title')
    abstract = elem.get('abstract')
    for phrase in processQueryResult(abstract):
        candidates.append(phrase) # what is your query?
import jieba
def getCuttedWords(phrase):
    candidates = jieba.lcut(phrase.lower())
    wordList = []
    for word in candidates:
        word = word.strip()
        if len(word)>0:
            wordList.append(word)
    return wordList
def countCommonWords(phrase_1, phrase_2, wordCount=False):
    words_1 = getCuttedWords(phrase_1)
    words_2 = getCuttedWords(phrase_2)
    # count for longest total length?
    result = list(set(words_1)&set(words_2))
    if wordCount:
        return len(result)
    else:
        return len("".join(result))
# candidates = list(set(candidates))

# candidates.sort(key=lambda phrase: -countCommonWords(phrase,query))
import Levenshtein
Levenshtein.distance(phrase, query)/ len()
# this sorting is wrong.
top_k = 20
print("TOP",top_k)
topKCandidates = candidates[:top_k]
topKCandidates.sort(key=lambda phrase: -len(phrase))
for elem in topKCandidates:
    print(elem)