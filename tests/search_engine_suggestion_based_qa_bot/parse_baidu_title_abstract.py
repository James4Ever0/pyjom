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
for elem in data:
    title = elem.get('title')
    abstract = elem.get('abstract')
    for phrase in processQueryResult(abstract):
        print(phrase)