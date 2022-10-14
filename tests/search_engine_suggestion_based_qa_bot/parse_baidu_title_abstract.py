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
def processQueryResult(abstract, minMaxDict={'min':5,'max':20}):
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
def countCommonCandidates(phrase_1,phrase_2):
    words_1 = set(getCuttedWords(phrase_1))
    words_2 =
    return len(list(set()&set()))

candidates.sort(key=lambda phrase: 