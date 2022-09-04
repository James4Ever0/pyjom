# funny sight.
# we plan to put automatic watermark detection here. no issue?
# import numpy as np
from pyjom.commons import *
from pyjom.mathlib import *
import cv2
# import cv2
def LRTBToDiagonal(lrtb):
    left, right, top, bottom = lrtb
    x0, y0, x1, y1 = left, top, right, bottom
    return (x0, y0, x1, y1)


def mergeAlikeRegions(sample, threshold=10):
    prevList = []
    newList = []
    import numpy as np

    def alike(array0, array1, threshold):
        npArray0, npArray1 = np.array(array0), np.array(array1)
        return max(abs(npArray0 - npArray1)) <= threshold

    newSample = []
    for item in sample:
        newItem = []
        for elem in item:
            for prevElem in prevList:
                if alike(prevElem, elem, threshold):
                    # mAlike = True
                    elem = prevElem.copy()
                    break
            newItem.append(elem.copy())
        # print(newItem) # showcase.
        newSample.append(newItem.copy())
        prevList = newItem.copy()
    return newSample


# import cv2
def getBlackPicture(width, height):
    blackPicture = np.zeros((height, width, 1), dtype="uint8")  # this is grayscale.
    return blackPicture


def getMergedRects(mConvList, width, height):
    blackPicture = getBlackPicture(width, height)
    for boundingBoxes in mConvList:
        # you might want to give them different weights?
        for boundingBox in boundingBoxes:
            # print("boundingBox:",boundingBox)
            # breakpoint()
            x0, y0, x1, y1 = [int(num) for num in boundingBox]
            p0 = (x0, y0)
            p1 = (x1, y1)
            cv2.rectangle(blackPicture, p0, p1, 255, -1)
    # newPicture = getBlackPicture(width, height)
    # cv2.imshow("IMAGE",blackPicture)
    # cv2.waitKey(100)

    contours = cv2.findContours(
        blackPicture, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    contours = contours[0] if len(contours) == 2 else contours[1]
    mlist = []
    for i in contours:
        x, y, w, h = cv2.boundingRect(i)
        mlist.append([x, y, w, h].copy())  # x,y,w,h!
    return mlist


def getVideoFrameSampler(videoPath, start, end, sample_size=60, iterate=False):
    cap = cv2.VideoCapture(videoPath)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    startFrame = int(start * fps)
    stopFrame = int(end * fps)
    import progressbar

    totalPopulation = list(range(startFrame, min(stopFrame, total_frames) - 1))
    samplePopulation = random.sample(
        totalPopulation, k=min(sample_size, len(totalPopulation))
    )
    samplePopulation.sort()
    if not iterate:
        imageList = []
    for sampleIndex in progressbar.progressbar(samplePopulation):
        cap.set(cv2.CAP_PROP_POS_FRAMES, sampleIndex)
        success, image = cap.read()
        if success:
            if iterate:
                yield image
            else:
                imageList.append(image.copy())
    if not iterate:
        return imageList


def getVideoFrameIterator(videoPath, start, end, sample_rate=1):
    cap = cv2.VideoCapture(videoPath)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    startFrame = int(start * fps)
    stopFrame = int(end * fps)
    # success, img = cap.read() # ignore first frame.
    # https://vuamitom.github.io/2019/12/13/fast-iterate-through-video-frames.html
    # to speed up the process we need to decompose the cap.read() method
    # and even better:
    # the official provides multithreading support. no thanks?
    import progressbar

    for fno in progressbar.progressbar(range(startFrame, stopFrame + 1, sample_rate)):
        if fno >= total_frames:
            break
        cap.set(cv2.CAP_PROP_POS_FRAMES, fno)
        success, image = cap.read()
        if success:
            yield image
        else:
            break
        # do_something(image)
    # fno = 0
    # while success:
    #     if fno % sample_rate == 0:
    #         # do_something(img)
    #         if fno > startFrame and fno < stopFrame:
    #             _, img = cap.retrieve()
    #             yield img
    #         if fno >= stopFrame:
    #             break
    #     # read next frame
    #     success, img = cap.grab()
    # cap.release()


def detectTextRegionOverTime(videoPath, start, end, sample_rate=10, mergeThreshold=10):
    iterator = getVideoFrameIterator(videoPath, start, end, sample_rate=sample_rate)
    detectionList = []
    # use some merging technique over time.
    # convolution?
    import easyocr

    reader = easyocr.Reader(["en"], gpu=True, recognizer=False)  # no metal? no dbnet18?
    # how many percent sure?
    # reader = easyocr.Reader(["en","ch_sim"],gpu=False, recognizer=False) # no metal? no dbnet18?
    # are you classifying the thing putting boxes into different category?
    # no it does not. first is detector, next is recognizer.
    # do not use recognizer here. for multiple reasons.
    noWHInfo = True
    width, height = None, None
    for index, frame in enumerate(iterator):
        if noWHInfo:
            noWHInfo = False
            height, width = frame.shape[:2]
        detection, recognition = reader.detect(frame)  # not very sure.
        if detection == [[]]:
            detectionList.append([])
            continue
        # print("frame number:",index)
        # for boundingBox in detection[0]:
        #     print(boundingBox) # left, right, top, bottom

        detectionList.append([LRTBToDiagonal(x) for x in detection[0]].copy())
        # print(detection)
        # breakpoint()
    del reader  # can it really free memory?
    # now we do some convolution.
    maxListIndex = len(detectionList)
    convSpan = 3
    finalRectList = []

    for index in range(maxListIndex):
        rangeStart, rangeEnd = index - convSpan, index + convSpan
        rangeStart, rangeEnd = max(0, rangeStart), min(maxListIndex, rangeEnd)
        mConvList = detectionList[rangeStart:rangeEnd]
        mergedRects = getMergedRects(mConvList, width, height)
        finalRectList.append(mergedRects.copy())

    newFinalRectList = mergeAlikeRegions(finalRectList, mergeThreshold)
    # incomplete. we need to get corresponding regions, and also nullsets.
    # using start and end to get these shit out.
    markers = np.linspace(start, end, len(newFinalRectList) + 1)
    ranges = list(zip(markers[:-1], markers[1:]))
    mRangesDict = {}
    for index, x in enumerate(newFinalRectList):
        for y in x:
            tupleY = tuple(y)
            mRangesDict.update({tupleY: mRangesDict.get(tupleY, []) + [ranges[index]]})
    # print(mRangesDict)
    # breakpoint()
    # why the fuck we have np.float64 as elem in mRangesDict's key(tuple)?
    newMRangesDict = {
        "delogo_{}_{}_{}_{}".format(*key): mRangesDict[key]  # x,y,w,h
        for key in mRangesDict.keys()
    }
    finalCatsMapped = getContinualMappedNonSympyMergeResult(
        newMRangesDict, noEmpty=True
    )  # need to use string input!
    return finalCatsMapped


def getPreviewPixels(defaultWidth, defaultHeight, maxPixel):
    mList = [defaultWidth, defaultHeight]
    # if defaultWidth < defaultHeight:
    #     reverseFlag = True
    maxDim = max(mList)
    shrinkRatio = maxPixel / maxDim
    getRounded = lambda num, rounder: (num // rounder) * rounder
    newFrameWork = [getRounded(x * shrinkRatio, 4) for x in mList]
    return newFrameWork[0], newFrameWork[1]


def getVideoWidthHeight(videoPath):
    from MediaInfo import MediaInfo

    info = MediaInfo(filename=videoPath)
    infoData = info.getInfo()
    # print(infoData)
    # breakpoint()
    defaultWidth = infoData["videoWidth"]
    defaultHeight = infoData["videoHeight"]
    return defaultWidth, defaultHeight


def getVideoPreviewPixels(videoPath, maxPixel=200):
    defaultWidth, defaultHeight = getVideoWidthHeight(videoPath)
    # print(infoData)
    # print(infoData.keys())
    # # breakpoint()
    # start = 0
    # end = float(infoData["videoDuration"])

    # maxPixel = 200

    previewWidth, previewHeight = getPreviewPixels(
        defaultWidth, defaultHeight, maxPixel
    )
    return previewWidth, previewHeight

def detectStationaryLogoOverTime():