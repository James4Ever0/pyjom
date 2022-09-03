import json
from test_commons import *
from pyjom.commons import *
import cv2
def getVideoPixels(videoPath):
    from MediaInfo import MediaInfo
    info = MediaInfo(filename = videoPath)
    infoData = info.getInfo()
    # print(infoData)
    # breakpoint()
    defaultWidth = infoData["videoWidth"]
    defaultHeight = infoData["videoHeight"]
    return defaultWidth, defaultHeight
# easy gig, you said.
# basePath = "/Users/jamesbrown/desktop/works/pyjom_remote"
basePath = "/root/Desktop/works/pyjom"
targetFile = basePath + "/tests/bilibili_practices/bilibili_video_translate/japan_day.json"

originalFile = basePath + "/tests/bilibili_practices/bilibili_video_translate/japan_day.webm"

# visualization can only be done here?
# where is the original file?

mJson = json.loads(open(targetFile, 'r',encoding='utf-8').read())
import numpy as np

width, height = getVideoPixels(originalFile)

def getBlackPicture(width, height):
    blackPicture =  np.zeros((height, width,1), dtype = "uint8") # this is grayscale.
    return blackPicture

mKeys = list(mJson.keys())
mIntKeys = [int(x) for x in mKeys]
minKey, maxKey = min(mIntKeys), max(mIntKeys)

# imutils is created by pyimagesearch.
from imutils.object_detection import non_max_suppression


def getConvBlurredCurrentShot(blurredSpan, span=5):
    # honor the most the latest one. 
    mImage = None
    for index, blurredImage in enumerate(blurredSpan):
        ratio = (span-index)/span
        if mImage is None:
            mImage = blurredImage*ratio
        else:
            mImage += mImage
    # print(mImage.shape)
    # breakpoint()
    return 256*((mImage>128).astype(np.uint8))


convolutionSpan = 5



convolutionBoundingBoxSpan = []
convolutionBlurredSpan = []



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
    blackPicture = getBlackPicture(width, height)
    for rectangle in flatSpan:
        # make it all int.
        x0,y0, x1, y1 = [int(num) for num in rectangle]
        loc0 = (x0,y0)
        loc1 = (x1,y1)
        cv2.rectangle(blackPicture, loc0, loc1, 255,cv2.FILLED) # we fill so we can merge shits.
    blackPictureBlurred =cv2.GaussianBlur(blackPicture, (33,33), 0)
    convolutionBlurredSpan.append(blackPictureBlurred.copy())

    if len(convolutionBlurredSpan) > convolutionSpan:
        convolutionBlurredSpan.pop(0)

    currentBlackPictureBlurred = getConvBlurredCurrentShot(convolutionBlurredSpan)
    # print(currentBlackPictureBlurred.shape)


    cv2.imshow("IMAGE", currentBlackPictureBlurred)
    cv2.waitKey(10)
    print("showing image:", intKey)
    print("boundingBoxes:", len(flatSpan))
    # print
    # cv2.waitKey(1000)
    # print("NON OVERLAPPING BOXES:")
    # print(currentNonOverlappingBoxes)
    # we need to visualize this shit.
    # breakpoint()
cv2.destroyAllWindows()
print("THE END")
