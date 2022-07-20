from .mediaDetector import *
import Levenshtein
import string
import zhon.hanzi
import wordninja

def resplitedEnglish(string2,skipSpecial=True):
    if skipSpecial:
        header = string2[0]
        if header in string.punctuation or header in zhon.hanzi.punctuation:
            return string2 # this could be buggy.
    result = wordninja.split(string2)
    if len(result)>1:
        mlist = zip(result[:-1], result[1:])
        for a,b in mlist:
            combined = "{} {}".format(a,b)
            error = a+b
            string2 = string2.replace(error,combined)
    return string2 # really? this is not good. maybe you should provide some version of continuality, for channel id watermarks.
    # @MA SECO. -> @MASECO

# maybe you can read it here?
# you need double language check. both chinese and english. or really?
def ocrEntityDetector(mdata):
    alteredData = [] # we should do a demo. 
    
    return alteredData # now we are on the same page, paddleocr is using cuda 11.2 which is compatible to 11.3

def getMinLenStr(a,b):
    la,lb = len(a),len(b)
    if la < lb:return a
    return b

def getBlockType(dlocation,dcontent):
    if not dlocation:
        if not dcontent: return "stationary"
        else: return "typing"
    else:
        if not dcontent: return "typing_moving"
        else: return "moving"

def getStringDistance(a,b):
    return Levenshtein.distance(a,b)

def getStringSimilarity(a,b):
    return Levenshtein.ratio(a,b)

def getChineseLen(string2):
    counter  = 0
    upperLimit, lowerLimit = 0x4e00, 0x9fff
    for elem in string2:
        ordNum = ord(elem)
        if ordNum <= upperLimit and ordNum>=lowerLimit:
            counter+=1
    return counter

def getPunctualLen(string2):
    counter = 0
    chinesePunctuals = zhon.hanzi.punctuation
    englishPunctuals = string.punctuation
    standardString = chinesePunctuals+englishPunctuals
    for elem in string2:
        if elem in standardString:
            counter+=2
    return counter


def getEnglishLen(string2):
    counter = 0
    standardString = "abcdefghijklmnopqrstuvwxyz"
    standardString += standardString.upper()
    standardString += "0123456789"
    # it won't split. you may need double check the thing.
    # standardString += " "
    for elem in string2:
        if elem in standardString:
            counter+=1
    return counter

def getMinMaxText(a,b):
    mlist = [a,b]
    clens = [getChineseLen(x) for x in mlist]
    elens = [getEnglishLen(x) for x in mlist]
    slens = [getPunctualLen(x) for x in mlist]
    mlens = [x[0]+x[1]+x[2] for x in zip(clens,elens,slens)]
    if len(a) > len(b):
        if mlens[0] > mlens[1]:
            return a
        return b
    else:
        if mlens[0] < mlens[1]:
            return b
        return a

def pointDifference(a,b):
    return [a[0] - b[0], a[1] - b[1]]

def makeOCREntity(ocrData,minMaxThresh = 24 ,# max difference is ten pixel. or it is considered as moving.
strDisThreshold = 2 ,# or considered as changing?
certThreshold = 0.6,
changingMinMaxThresh = 45,
changingstrDisThreshold = 3,
timeThreshold = 0.3 ,# i intentially set it.
blockTimeThreshold = 0.3, # at least last this long?
strSimThreshold = 0.8):
    testElemIds = {} # just show processed items.
    for line in ocrData:
        mtime,mframe,mresult = line["time"],line["frame"],line["paddleocr"]
        # print("______________________")
        # print("time:",mtime)
        # newlyAddedIds = [] # will directly added if not in.
        # initiate things here.
        for mid in testElemIds.keys(): # must trt
            testElemIds[mid]["hasIdentical"] =False  #initialization.
        for presult in mresult:
            location, mtext = presult
            p1, p2, p3, p4 = location
            text, certainty = mtext
            print("RECOGNIZED TEXT:",text)
            mtimestamp = {"frame":mframe,"time":mtime}
            # print("location:",location)
            # print("text:",text)
            # print("certainty:",certainty)
            foundIdentical = False
            for mid in testElemIds.keys():
                myid = testElemIds[mid]
                myLastLocation = myid["locations"][-1]
                px1,px2,px3,px4 = myLastLocation
                myMinMax = max([max(pointDifference(a,b)) for a,b in zip(location,myLastLocation)])
                myMinMaxs = [max([max(pointDifference(a,b)) for a,b in zip(location,myLL)]) for myLL in myid["locations"]] # changing it. the max movement.
                mLastTime = myid["timestamps"][-1]["time"]
                timeDelta = mLastTime - mtime
                myLastContent = myid["contents"][-1]
                strDistance = getStringDistance(myLastContent,text)
                strDistances = [getStringDistance(myLastContent,text) for myLC in myid["contents"]]
                strSim = getStringSimilarity(myLastContent,text)
                strSims = [getStringSimilarity(myLC,text) for myLC in myid["contents"]]
                foundIdentical = False

                movementMap = {"location":False,"content":False,"continual":False}
                if timeDelta < timeThreshold:
                    if myMinMax <= minMaxThresh and ((strDistance <= strDisThreshold) or (strSim >= strSimThreshold )) : # wrong logic.
                        foundIdentical = True
                        
                        print("test result:",myMinMax <= minMaxThresh ,(strDistance <= strDisThreshold) , (strSim >= strSimThreshold ))
                        print(myMinMax,strDistance,strSim)
                        print(minMaxThresh,strDisThreshold,strSimThreshold)
                        print("line a")
                        pass
                        # stricter limit, to know if really is movement?
                    elif myMinMax <= changingMinMaxThresh:
                        foundIdentical = True

                        movementMap["location"] = True
                        if max(strDistances) <= strDisThreshold or max(strSims) >= strSimThreshold:
                            # make sure it is globally the same.
                            print("line b")
                            pass
                        elif min(strDistances) <= changingstrDisThreshold:
                            print("line c")
                            movementMap["content"] = True
                        else: # consider something else
                            print("line d")
                            foundIdentical = False
                    elif strDistance <= changingstrDisThreshold or strSim >= strSimThreshold:
                        foundIdentical = True

                        print("line e")
                        movementMap["content"] = True
                        if max(myMinMaxs) <= minMaxThresh:
                            print("line f")
                            pass
                        elif min(myMinMaxs) <= changingMinMaxThresh:
                            print("line g")
                            movementMap["location"] = True
                        else:
                            print("line h")
                            foundIdentical = False
                else:
                    foundIdentical = False
                if foundIdentical:
                    print("FOUND IDENTICAL",text,myLastContent)
                    print("REASON",movementMap)
                    print("ID",mid)
                    print()
                    # care about continuality here.
                    if timeDelta < timeThreshold:
                        movementMap["continual"] = True
                    if myid["hasIdentical"] or timeDelta == 0: # eliminate duplicates.
                        continue # do not check this.
                    # print("found Identical:",mid)
                    testElemIds[mid]["hasIdentical"]=True
                    testElemIds[mid]["locations"].append(location)
                    testElemIds[mid]["contents"].append(text)
                    testElemIds[mid]["timestamps"].append(mtimestamp)
                    testElemIds[mid]["movements"].append(movementMap)
                    break
            if not foundIdentical:
                if certainty > certThreshold:
                    minitStruct = {str(uuid.uuid4()):{"locations":[copy.deepcopy(location)],"contents":[copy.deepcopy(text)],"movements":[],"hasIdentical":False,"timestamps":[mtimestamp]}}
                    testElemIds.update(minitStruct) # do you really expect it? i mean it could have cracks.
    # print(json.dumps(testElemIds,indent=4))
    keys= list(testElemIds.keys())
    print("keyNum:",len(keys))
    mfinal = {}
    for key in keys:
        mblocks = []
        kElem = testElemIds[key]
        # we try to compress this thing.
        initBlock = {"type":"stationary","text":None,"location":None,"timespan":{"start":None,"end":None}} # we will have shortest text.
        for index, mtimestamp in enumerate(kElem["timestamps"]):
            thisText = kElem["contents"][index]
            thisLocation = kElem["locations"][index]
            if index == 0:
                initBlock["timespan"]["start"] = mtimestamp
                initBlock["timespan"]["end"] = mtimestamp
                initBlock["text"] = thisText
                initBlock["location"] = copy.deepcopy(thisLocation)
            else:
                movementMap = kElem["movements"][index-1]
                dlocation, dcontent, dtime = movementMap["location"], movementMap["content"], movementMap["continual"]
                lastType = initBlock["type"]
                thisType = getBlockType(dlocation,dcontent)

                if (not dtime) or (thisType != lastType):
                    # will abandon all no matter what. cause it is not continual.
                    mblocks.append(copy.deepcopy(initBlock))
                    initBlock = {"type":thisType,"timespan":{"start":mtimestamp,"end":mtimestamp}} # get the content.
                    if thisType in ["stationary", "moving"]:
                        # lastText = initBlock["text"]
                        # mselectedText = getMinMaxText(lastText,thisText)
                        initBlock.update({"text":thisText}) # not right. we select the best one.
                    if thisType in ["stationary", "typing"]:
                        initBlock.update({"location":copy.deepcopy(thisLocation)})
                    if thisType in ["typing_moving","typing"]:
                        initBlock.update({"texts":[thisText]})
                    if thisType in ["moving", "typing_moving"]:
                        initBlock.update({"locations":[copy.deepcopy(thisLocation)]})
                else:
                    initBlock["timespan"]["end"] = mtimestamp
                    if thisType in ["moving","typing_moving"]:
                        initBlock["locations"].append(copy.deepcopy(thisLocation))
                    if thisType in ["typing_moving","typing"]:
                        initBlock["texts"].append(thisText)
                    if thisType in ["moving","stationary"]: # we don't change stationary/typing's location. or do we?
                        mLastText = initBlock["text"]
                        initBlock["text"] = getMinMaxText(mLastText,thisText)
                        # initBlock["text"] = getMinLenStr(mLastText,thisText)
        mblocks.append(copy.deepcopy(initBlock))
        mblocks2 = []
        for block in mblocks:
            start,end = block["timespan"]["start"], block["timespan"]["end"]
            timedelta = end["time"] - start["time"]
            if timedelta > blockTimeThreshold:
                mblocks2.append(block)
        mfinal.update({key:mblocks2})
    return mfinal
    # print(json.dumps(mfinal,indent=4))
    # print("___________")


def staticOCRCombinator(myresult,simThreshold= 0.8):
    # we use wordninja to do the english spliting.
    # you can also get this working for non-static.
    myNewResult = {}
    lastWordResult = None
    lastId = None
    lastLocation = None
    lastTimeStamp = {"start":{},"end":{}}
    for key in myresult.keys():
        melems = myresult[key]
        for melem in melems:
            mtype = melem["type"]
            if mtype in ["stationary", "moving"]:
                mtext = melem["text"] # maybe there are some moving things out there?
            else:
                mtext = melem["texts"][0]
            mtext = resplitedEnglish(mtext)
            if lastWordResult is None:
                lastWordResult = mtext
                lastId = key
                lastTimeStamp["start"] = melem["timespan"]["start"]
                lastTimeStamp["end"] = melem["timespan"]["end"]
                if mtype in ["stationary", "typing"]:
                    lastLocation = melem["location"]
                else:
                    lastLocation = melem["locations"][0]
            else:
                if getStringSimilarity(lastWordResult,mtext) > simThreshold:
                    # merge the thing.
                    lastTimeStamp["start"] = list(sorted([melem["timespan"]["start"],lastTimeStamp["start"]],key=lambda x:x["time"]))[0]
                    lastTimeStamp["end"] = list(sorted([melem["timespan"]["end"],lastTimeStamp["end"]],key=lambda x:-x["time"]))[0]
                else:
                    myNewResult.update({lastId:{"content":lastWordResult,"timespan":lastTimeStamp,"location":lastLocation}})
                    lastWordResult = mtext
                    lastId = key
                    if mtype in ["stationary", "typing"]:
                        lastLocation = melem["location"]
                    else:
                        lastLocation = melem["locations"][0]
                    lastTimeStamp["start"] = melem["timespan"]["start"]
                    lastTimeStamp["end"] = melem["timespan"]["end"]
            # else:
            #     print("found different type:",mtype)
            #     print("text:",mtext)
            #     print("element:",melem)
    myNewResult.update({lastId:{"content":lastWordResult,"timespan":lastTimeStamp,"location":lastLocation}})
    print("process complete")
    return myNewResult