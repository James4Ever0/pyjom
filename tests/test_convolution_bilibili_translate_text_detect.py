import json
def getVideoPixels(videoPath):
    from MediaInfo import MediaInfo
    info = MediaInfo(filename = videoPath)
    infoData = info.getInfo()
    # print(infoData)
    # breakpoint()
    defaultWidth = infoData["videoWidth"]
    defaultHeight = infoData["videoHeight"]
# easy gig, you said.
basePath = "/root/Desktop/works/pyjom"
targetFile = basePath + "/tests/bilibili_practices/bilibili_video_translate/japan_day.json"

originalFile = basePath + "/tests/bilibili_practices/bilibili_video_translate/japan_day.webm"

# visualization can only be done here?
# where is the original file?

mJson = json.loads(open(targetFile, 'r',encoding='utf-8').read())
import numpy as np


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
            npLocation = np.array(location)
            xlocs = npLocation[:,0]
            ylocs = npLocation[:,1]
            # print(xlocs)
            # print(ylocs)
            # breakpoint()
            minX, maxX = min(xlocs), max(xlocs)
            minY, maxY = min(ylocs), max(ylocs)
            boundingBox = [minX, minY, maxX, maxY]
            boundingBoxes.append(boundingBox.copy())
            # breakpoint()
        # print("text", text)
        # print("confidence", confidence)
    convolutionBoundingBoxSpan.append(boundingBoxes.copy())
    if len(convolutionBoundingBoxSpan)> convolutionSpan:
        convolutionBoundingBoxSpan.pop(0)
    # do your calculation!
    flatSpan = [y for x in convolutionBoundingBoxSpan for y in x]
    flatSpan = np.array(flatSpan)
    currentNonOverlappingBoxes = non_max_suppression(flatSpan)
    # print(intKey,target)
    # this time we do not care about the text inside.
    # print("NON OVERLAPPING BOXES:")
    # print(currentNonOverlappingBoxes)
    # we need to visualize this shit.
    # breakpoint()
