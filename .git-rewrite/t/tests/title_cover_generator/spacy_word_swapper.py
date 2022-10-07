# just use some simple analysis to extract the template. may not be cost effective like DianJing also you can try the freaking gpt2 model, or pegasus.
from commons import sample_data

# first assume all to be freaking chinese.
# import nltk
import spacy
import jieba
from spacy.lang.zh.examples import sentences 

import re

def recursiveCompiledSearch(compiledRegex, pattern,initPos=0,resultTotal = []):
    result = compiledRegex.search(pattern)
    if result !=None:
        match = result[0]
        span = result.span()
        realSpan = (span[0]+initPos, span[1]+initPos)
        # initialSpan = span[0]
        endSpan = span[1]
        initPos += endSpan
        mresult = {"match":match, "span":realSpan}
        resultTotal.append(mresult)
        newPattern = pattern[endSpan:]
        return recursiveCompiledSearch(compiledRegex,newPattern,initPos,resultTotal)
    else: return resultTotal

nlp = spacy.load("zh_core_web_sm")
# proper_nouns = ['守望先锋','第五人格']
# whatever. we can always change shit.
# nlp.tokenizer.pkuseg_update_user_dict(proper_nouns)
# this is imoortant.
english = re.compile(r"([a-zA-Z]+([ \-,\.:;?!]+)?)+")

def check_has_language(string,language_re): result = recursiveCompiledSearch(language_re,string,resultTotal=[]); return len(result) >0
for elem in sample_data:
    hasSpace = False
    # we need to eliminate some english things.
    # we also have some spaces. remove them before proceed.
    if " " in elem:
        hasSpace = True
        elem = elem.replace(" ", "")
    # some flashy text will never be accepted. if outside of english, chinese we accept nothing.
    # english is not included in spacy.
    data = [x for x in jieba.cut(elem)] # contradictory.
    english_check = check_has_language(elem,english)
    if english_check:
        print("HAS ENGLISH")
        print(elem)
        continue
    # check if words contains english. remove these titles.
    # print(data)
    nlp.tokenizer.pkuseg_update_user_dict(data)
    doc = nlp(elem)
    print(doc.text)
    for token in doc:
        print(token.text, token.pos_, token.dep_)
