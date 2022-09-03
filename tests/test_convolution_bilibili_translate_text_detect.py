import json

# easy gig, you said.
targetFile = "/root/Desktop/works/pyjom/tests/bilibili_practices/bilibili_video_translate/japan_day.json"

mJson = json.loads(open(targetFile, 'r',encoding='utf-8').read())

mKeys = list(mJson.keys())
mIntKeys = [int(x) for x in mKeys]
minKey, maxKey = min(mIntKeys), max(mIntKeys)

# imutils is created by pyimagesearch.
from imutils.object_detection import non_max_suppression

convolutionSpan = 5

convolutionBoundingBoxSpan = []

for intKey in range(minKey, maxKey+1):
    strKey = str(intKey)
    target = mJson[strKey]
    boundingBoxes = []
    for item in target:
        location = item[0]
        text, confidence = item[1]
        # print("location",location) # four points. do not know if there is any rotation here.
        if confidence > 0.7:
            xlocs = location[:,0]
            ylocs = location[:,1]
            minX, maxX = min(xlocs), max(xlocs)
            minY, maxY = min(ylocs), max(ylocs)
            boundingBox = [minX, minY, maxX, maxY]
            boundingBoxes.append(boundingBox.copy())
        # print("text", text)
        # print("confidence", confidence)
    convolutionBoundingBoxSpan.append(boundingBoxes.copy())
    if len(convolutionBoundingBoxSpan)> convolutionSpan:
        convolutionBoundingBoxSpan.pop(0)
    # do your calculation!
    
    # print(intKey,target)
    # this time we do not care about the text inside.
    # breakpoint()