from lazero.filesystem.io import readJsonObjectFromFile
from lazero. import checkMinMaxDict
data = readJsonObjectFromFile('result_baidu.json')
import string
from zhon import hanzi
for elem in data:
    title = elem.get('title')
    abstract = elem.get('abstract')
    punctuations = set(list(string.punctuation+hanzi.punctuation))
    punctuations.remove(" ")
    for punc in punctuations:
        abstract = abstract.replace(punc, "\n")
    abstract = abstract.split("\n")
    for phrase in abstract:
        if not checkMinMaxDict(len(phrase), minMaxDict):
    return abstract