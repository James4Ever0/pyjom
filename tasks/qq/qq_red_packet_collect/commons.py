import random
import re
from string import punctuation
from base_opq import stderrPrint

def keywordDecorator(func, **kwargs2):
    def mytarget(*margs, **kwargs):
        if "trace_source" in kwargs.keys():
            if kwargs2["trace_source"]:
                return func(*margs, **kwargs, **kwargs2), ".".join(
                    [__name__, func.__name__]
                )
        return func(*margs, **kwargs, **kwargs2)

    return mytarget

def replaceDuplicateChar(sentence: str, char=" ", maxRepeat: int = 3):
    assert maxRepeat >= 0
    source = char * (maxRepeat + 1)
    target = char * maxRepeat
    # c=0
    while True:
        # c+=1
        # stderrPrint("RETRYING",c)
        if source in sentence:
            # stderrPrint(len(source), len(target))
            sentence = sentence.replace(source, target)
        else:
            break  # freaking important!
    return sentence


def replaceDuplicateChars(sentence: str, maxRepeat: int = 3):
    chars = set(list(sentence))
    for char in chars:
        sentence = replaceDuplicateChar(sentence, char, maxRepeat=maxRepeat)
    return sentence


def replaceDuplicateWords(sentence: str):
    # TODO: remove duplicate words inside, using jieba.
    # TODO: collect the candidateWordList from chat history.
    # TODO: force replace mode: at least replace (n) words inside sentence
    # TODO: mark words as replaceble by word type.
    pass


def cutIncompleteSentenceTail(
    sentence: str, threshold: int = len("这个群是我老公，你要是让我管管你老公")):  # wtf?
    if len(sentence) > threshold:
        pun = "，。……——“”‘’！； " + punctuation  # with english space and puncs.
        punList = list(set(list(pun)))
        pattern = re.compile("|".join(
            [re.escape(punctualChar) for punctualChar in punList]))
        resultList = re.split(pattern, sentence)
        resultList = [x for x in resultList if len(x) > 0]
        for index in range(
                1,
                len(resultList)):  # will return first sentence nevertheless.
            if pattern.match(resultList[-index]):  # suspected punctual element.
                sentence = "".join(resultList)[:-index]
                return sentence
        sentence = resultList[0]  # failsafe.
    return sentence


def generatedSentenceFixer(sentence,
                           threshold=len("这个群是我老公，你要是让我管管你老公"),
                           maxRepeat=3):
    sentence = replaceDuplicateChars(sentence, maxRepeat=maxRepeat)
    sentence = cutIncompleteSentenceTail(sentence, threshold=threshold)
    return sentence


def weightedRandomYielder(elemList: list,
                          elemWeights: list,
                          shuffle=True,
                          no_repeat=True,
                          single=False):
    assert len(elemList) >= 2
    assert len(elemWeights) == len(elemList)
    baseList = []
    for elem, weight in zip(elemList, elemWeights):
        assert weight > 0
        assert type(weight) == int
        baseList += [elem] * weight
    if shuffle:
        random.shuffle(baseList)
    usedElem = []
    for elem in baseList:
        if single: return elem
        if not no_repeat: yield elem
        elif elem in usedElem:
            continue
        else:
            usedElem.append(elem)
            yield elem