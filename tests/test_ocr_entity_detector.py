from test_commons import *
from pyjom.medialang.functions.detectors.entityDetector import *
import json

# check if text is movement or we have to mark its trajectory.
# feeling like i am a game maker.

dataPath = "/root/Desktop/works/pyjom/logs/local/1649678716_663207.json"

mdata = open(dataPath, "r", encoding="utf8").read()
mdata = json.loads(mdata)
# minMaxThresh = 14 # max difference is ten pixel. or it is considered as moving.
# strDisThreshold = 1 # or considered as changing?
# certThreshold = 0.7
# changingMinMaxThresh = 25
# changingstrDisThreshold = 2
# timeThreshold = 0.3 # i intentially set it.
# blockTimeThreshold = 0.3 # at least last this long?
# strSimThreshold = 0.8


# print(mtext, key) # this is stationary.

for elem in mdata:
    # maybe something in a sequence? like location similarity?
    # if location is similar, but text is different, do we really need to handle it?
    # we need to collect similar frames, so we can deduct further.
    try:
        rev = elem["review"]["review"][1]
        ocrData = rev["subtitle_detector"]["subtitle_result"]["paddleocr"]
        # here is the core.
        myresult = makeOCREntity(ocrData, blockTimeThreshold=0, timeThreshold=0.1)
        myNewResult = staticOCRCombinator(myresult)  # this is forced combination.
        # print(json.dumps(myNewResult,indent=4))
        for key in myNewResult.keys():
            myElem = myNewResult[key]
            print(myElem["content"], key)
        breakpoint()
    except:
        import traceback

        traceback.print_exc()
        breakpoint()
