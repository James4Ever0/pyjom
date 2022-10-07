# target = "sample_strings.txt"

# data = open(target,"r",encoding="utf-8").read()
# data = data.split("\n")

from zhon.hanzi import characters, radicals, punctuation
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

from itertools import groupby, count

def set_to_range(numberlist):
    numberlist = list(sorted(numberlist)) # double safety?
    gpb = groupby(numberlist, lambda n, c=count(): n-next(c))

    # Then to finish it off, generate the string from the groups.

    def as_range(iterable): # not sure how to do this part elegantly
        l = list(iterable)
        if len(l) > 1:
            return (l[0], l[-1]+1)
        else:
            return (l[0], l[0]+1)

    result = [as_range(g) for _, g in gpb]
    # result = [as_range(g) for _, g in groupby(numberlist, key=lambda n, c=count(): n-next(c))]
    return result
    # '1-3,6-7,10'
import uuid

def get_myuuid(): return str(uuid.uuid4())

def get_chinese_result(line,chineseSet):
    chineseRanges = set_to_range(chineseSet)
    result = []
    for r in chineseRanges:
        text = line[r[0]:r[1]]
        data = {"match":text,"span":r,"lang":"zh","uuid":get_myuuid()}
        result.append(data)
    return result


all_chinese = characters+radicals+punctuation

english = re.compile(r"([a-zA-Z]+([ \-,\.:;?!]+)?)+")

# for line in data:
def analyze_mixed_text(line):
    line = line.replace("\n","")
    # if len(line) <=3: continue
    # shall we analyze this shit line by line?
    # just a fucking try...
    print("LINE DATA: " + line)
    eng_result = recursiveCompiledSearch(english,line,initPos=0,resultTotal = []) # recursive curse.
    engSet = []
    engResult = []
    for eng in eng_result:
        print("FOUND ENGLISH: ", eng)
        span = eng["span"]
        mword = line[span[0]:span[1]]
        mrange = list(range(span[0],span[1]))
        engSet += mrange
        eng2 = eng
        eng2.update({"lang":"en","uuid":get_myuuid()})
        engResult.append(eng2)
        print("VERIFICATION:",mword)
    chineseSet = [x for x in range(len(line)) if x not in engSet]
    chineseResult = get_chinese_result(line,chineseSet)
    finalResult = chineseResult+engResult
    finalResult = sorted(finalResult,key=lambda x:x["span"][0])
    result = {"en":[],"zh":[]}
    for index, data in enumerate(finalResult):
        lang = data["lang"]
        text = data["match"]
        result[lang].append({"index":index,"text":text})
    return result