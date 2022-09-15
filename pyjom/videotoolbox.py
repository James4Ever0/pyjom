# funny sight.
# we plan to put automatic watermark detection here. no issue?
# import numpy as np
from pyjom.commons import *
from pyjom.mathlib import *
import cv2
from pyjom.imagetoolbox import *

# import cv2

def getEffectiveFPS(videoPath, convert_fps_target=15):
    return effectiveFPS

def getVideoColorCentrality(videoPath,
denoise=True,
sample_size_limit=5000,
    epsilon=0.01,  # shit man.
    shift=2,
    n_clusters=5,
    batch_size=45,
    max_no_improvement=10):
    return centrality, max_nearby_center_percentage,centrality, max_nearby_center_percentage


def checkXYWH(XYWH, canvas, minArea=20):
    import math
    x, y, w, h = XYWH
    width, height = canvas
    if x >= width - 1 or y >= height - 1:
        return False, None
    if x == 0:
        x = 1
    if y == 0:
        y = 1
    if x + w >= width:
        w = width - x - 1
        w = math.floor(w/2)*2
        if w <= 2:
            return False, None
    if y + h >= height:
        h = height - y - 1
        h = math.floor(h/2)*2
        if h <= 2:
            return False, None
    if w * h <= minArea:
        return False, None
    return True, (x, y, w, h)


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
    # this is grayscale.
    blackPicture = np.zeros((height, width, 1), dtype="uint8")
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
    # if not iterate:
    # print("NOT ITERATING")

    def nonIterator(cap, samplePopulation):
        imageList = []
        for sampleIndex in progressbar.progressbar(samplePopulation):
            cap.set(cv2.CAP_PROP_POS_FRAMES, sampleIndex)
            success, image = cap.read()
            if success:
                # print("APPENDING!")
                imageList.append(image.copy())
        return imageList

    def iterator(cap, samplePopulation):
        for sampleIndex in progressbar.progressbar(samplePopulation):
            cap.set(cv2.CAP_PROP_POS_FRAMES, sampleIndex)
            success, image = cap.read()
            if success:
                # print("APPENDING!")
                # imageList.append(image.copy())
                yield image

    if iterate:
        return iterator(cap, samplePopulation)
    else:
        return nonIterator(cap, samplePopulation)


def getVideoFrameIterator(videoPath, start, end, sample_rate=1, batch=1):
    assert batch >= 1
    assert sample_rate >= 1
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
        fnoMax = fno+batch-1
        if fnoMax >= total_frames:
            break
        for fnoX in range(batch):
            cap.set(cv2.CAP_PROP_POS_FRAMES, fnoX+fno)
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


def detectTextRegionOverTime(videoPath, start, end, sample_rate=3, mergeThreshold=10): # this sample rate is too unreasonable. set it to 3 or something.
    iterator = getVideoFrameIterator(
        videoPath, start, end, sample_rate=sample_rate)
    detectionList = []
    # use some merging technique over time.
    # convolution?
    import easyocr

    # no metal? no dbnet18?
    reader = easyocr.Reader(["en"], gpu=True, recognizer=False)
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
            mRangesDict.update(
                {tupleY: mRangesDict.get(tupleY, []) + [ranges[index]]})
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
    def getRounded(num, rounder): return (num // rounder) * rounder
    newFrameWork = [getRounded(x * shrinkRatio, 4) for x in mList]
    return newFrameWork[0], newFrameWork[1]


def getVideoFrameRate(videoPath):
    from MediaInfo import MediaInfo

    info = MediaInfo(filename=videoPath)
    infoData = info.getInfo()
    return float(infoData["videoFrameRate"])


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


def detectStationaryLogoOverTime(filepath, start, end, sample_size=60, cornersOnly=True, areaThreshold = 30):
    imageSet = getVideoFrameSampler(
        filepath, start, end, sample_size=sample_size)
    # what is this src?
    # from src import *
    defaultWidth, defaultHeight = getVideoWidthHeight(filepath)

    deltaWidthRatio = 4+(4-3)*(defaultWidth/defaultHeight-16/9)/(16/9-9/16)
    deltaWidthRatio = makeValueInRange(deltaWidthRatio,3,4)
    deltaHeightRatio = 8+(8-6)*(defaultHeight/defaultWidth-16/9)/(16/9-9/16)
    deltaHeightRatio = makeValueInRange(deltaHeightRatio,6,8)
    deltaWidth, deltaHeight = int(defaultWidth/deltaWidthRatio), int(defaultHeight/deltaHeightRatio)
    # (x1, y1), (x2, y2)
    fourCorners = [
        [(0,0),(deltaWidth, deltaHeight)],
        [(defaultWidth-deltaWidth,0),(defaultWidth, deltaHeight)],
        [(defaultWidth-deltaWidth, defaultHeight-deltaHeight),(defaultWidth, defaultHeight)],
        [(0,defaultHeight-deltaHeight),(deltaWidth, defaultHeight)]
    ]

    ###########
    import sys
    import os
    import cv2
    import numpy as np
    import warnings
    from matplotlib import pyplot as plt
    import math
    import numpy
    import scipy
    import scipy.fftpack

    # Variables
    KERNEL_SIZE = 3

    def estimate_watermark_imgSet(imgset):
        """
        Given a folder, estimate the watermark (grad(W) = median(grad(J)))
        Also, give the list of gradients, so that further processing can be done on it
        """
        images = imgset

        # Compute gradients
        print("Computing gradients.")
        gradx = list(
            map(lambda x: cv2.Sobel(x, cv2.CV_64F, 1, 0, ksize=KERNEL_SIZE), images)
        )  # this is py3 my friend?
        grady = list(
            map(lambda x: cv2.Sobel(x, cv2.CV_64F, 0, 1, ksize=KERNEL_SIZE), images)
        )  # this is py3 my friend?

        # Compute median of grads
        print("Computing median gradients.")
        # print(gradx,grady)
        # breakpoint()
        Wm_x = np.median(np.array(gradx), axis=0)
        Wm_y = np.median(np.array(grady), axis=0)
        # slow as hell?

        return (Wm_x, Wm_y, gradx, grady)

    def poisson_reconstruct(
        gradx,
        grady,
        kernel_size=KERNEL_SIZE,
        num_iters=100,
        h=0.1,
        boundary_image=None,
        boundary_zero=True,
    ):
        """
        Iterative algorithm for Poisson reconstruction.
        Given the gradx and grady values, find laplacian, and solve for image
        Also return the squared difference of every step.
        h = convergence rate
        """
        fxx = cv2.Sobel(gradx, cv2.CV_64F, 1, 0, ksize=kernel_size)
        fyy = cv2.Sobel(grady, cv2.CV_64F, 0, 1, ksize=kernel_size)
        laplacian = fxx + fyy
        m, n, p = laplacian.shape  # three channels?

        if boundary_zero == True:
            est = np.zeros(laplacian.shape)
        else:
            assert boundary_image is not None
            assert boundary_image.shape == laplacian.shape
            est = boundary_image.copy()

        est[1:-1, 1:-1, :] = np.random.random((m - 2, n - 2, p))
        loss = []

        for i in range(num_iters):
            old_est = est.copy()
            est[1:-1, 1:-1, :] = 0.25 * (
                est[0:-2, 1:-1, :]
                + est[1:-1, 0:-2, :]
                + est[2:, 1:-1, :]
                + est[1:-1, 2:, :]
                - h * h * laplacian[1:-1, 1:-1, :]
            )
            error = np.sum(np.square(est - old_est))
            loss.append(error)

        return est

    ###########
    # you can do this later, will you?
    gx, gy, gxlist, gylist = estimate_watermark_imgSet(imageSet)
    # print(gx.shape, gy.shape)
    # breakpoint() # nothing here! fuck.
    # print(len(imageSet))
    # cropped_gx, cropped_gy, watermark_location = crop_watermark(gx, gy,location=True)

    # W_m = poisson_reconstruct(cropped_gx, cropped_gy)

    W_full = poisson_reconstruct(gx, gy)

    maxval, minval = np.max(W_full), np.min(W_full)
    W_full = (W_full - minval) * \
        (255 / (maxval - minval))  # is that necessary?
    # # print(,W_full.shape,W_full.dtype)
    W_full = W_full.astype(np.uint8)

    src = W_full
    scale_percent = 100

    # calculate the 50 percent of original dimensions
    width = int(src.shape[1] * scale_percent / 100)
    height = int(src.shape[0] * scale_percent / 100)

    # dsize
    dsize = (width, height)

    # resize image
    output = cv2.resize(src, dsize)

    gray_output = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)

    gray_output = cv2.GaussianBlur(gray_output, (11, 3), 0)

    thresh_output = cv2.adaptiveThreshold(
        gray_output, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    )

    thresh_output = 255 - thresh_output

    # cnts, hierachy = cv2.findContours(thresh_output,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) # really freaking bad. we should invert this.
    cnts, hierachy = cv2.findContours(
        thresh_output, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )  # really freaking bad. we should invert this.
    # cv2.RETR_EXTERNAL

    [a, b] = output.shape[:2]
    myMask = np.zeros(shape=[a, b], dtype=np.uint8)

    # this is for video watermarks. how about pictures? do we need to cut corners? how to find the freaking watermark again?
    for cnt in cnts:
        x, y, w, h = cv2.boundingRect(cnt)  # Draw the bounding box image=
        # cv2.rectangle(output, (x,y), (x+w,y+h), (0,0,255),2)
        cv2.rectangle(myMask, (x, y), (x + w, y + h), 255, -1)

    dilated_mask = cv2.GaussianBlur(myMask, (11, 11), 0)
    cv2.threshold(dilated_mask, 256 / 2, 255, cv2.THRESH_BINARY, dilated_mask)
    cnts2, hierachy2 = cv2.findContours(
        dilated_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    myMask2 = np.zeros(shape=[a, b], dtype=np.uint8)

    # this is for video watermarks. how about pictures? do we need to cut corners? how to find the freaking watermark again?
    # delogoFilter =
    mFinalDelogoFilters = []
    for cnt in cnts2:
        x, y, w, h = cv2.boundingRect(cnt)  # Draw the bounding box image=
        currentRect = [(x,y),(x+w,y+h)]
        if cornersOnly:
            for cornerRect in fourCorners:
                overlapRect = getOverlapRect(currentRect, cornerRect)
                if overlapRect:
                    (x0,y0),(x1,y1) = overlapRect
                    x,y,w,h = x0,y0, x1-x0, y1-y0
                    area = w*h
                    if area < areaThreshold:
                        continue
                    delogoCommand = "delogo_{}_{}_{}_{}".format(x, y, w, h)
                    # print(delogoCommand)
                    # print('width:{} height:{}'.format(b,a))
                    mFinalDelogoFilters.append(delogoCommand)
        else:
            if area < areaThreshold:
                continue
            delogoCommand = "delogo_{}_{}_{}_{}".format(x, y, w, h)
            mFinalDelogoFilters.append(delogoCommand)
        # cv2.rectangle(output, (x,y), (x+w,y+h), (0,0,255),2)
        # cv2.rectangle(myMask2, (x, y), (x + w, y + h), 255, -1)
    print("TOTAL {} STATIONARY LOGOS.".format(len(cnts2)))
    # breakpoint()
    # get the final dictionary
    if len(mFinalDelogoFilters) == 0:
        return {}
    else:
        delogoCommandSet = "|".join(mFinalDelogoFilters)
        # print(delogoCommandSet)
        # breakpoint()
        return {delogoCommandSet: [(start, end)]}


def sampledStablePipRegionExporter(data, defaultWidth, defaultHeight, shrink=0.8):
    defaultWidth, defaultHeight = int(defaultWidth), int(defaultHeight)
    import numpy as np

    data = np.array(data)

    def getAlikeValueMerged(mArray, threshold=35):
        for index, elem in enumerate(mArray[:-1]):
            nextElem = mArray[index + 1]
            if abs(nextElem - elem) < threshold:
                mArray[index + 1] = elem
        return mArray

    def listToRangedDictWithLabel(mList, label):
        resultDict = {}
        for index, elem in enumerate(mList):
            mKey = "{}:{}".format(label, int(elem))
            resultDict.update(
                {mKey: resultDict.get(mKey, []) + [(index, index + 1)]})
        return resultDict

    def pointsToRangedDictWithLabel(mArray, label, threshold=35, method='kalman'):
        assert method in ['ema', 'kalman']
        if method == 'ema':
            mArray = get1DArrayEMA(mArray)  # to kalman?
        else:
            mArray = Kalman1D(mArray, damping=0.1)
        mArray = getAlikeValueMerged(mArray, threshold=threshold)
        return listToRangedDictWithLabel(mArray, label)

    threshold = max(35, int(max(defaultWidth, defaultHeight) * 0.02734375))
    # threshold =
    mPoints = [data[:, 0, 0], data[:, 0, 1], data[:, 1, 0], data[:, 1, 1]]
    xLeftPoints = pointsToRangedDictWithLabel(
        data[:, 0, 0], "xleft", threshold=threshold
    )
    yLeftPoints = pointsToRangedDictWithLabel(
        data[:, 0, 1], "yleft", threshold=threshold
    )
    xRightPoints = pointsToRangedDictWithLabel(
        data[:, 1, 0], "xright", threshold=threshold
    )
    yRightPoints = pointsToRangedDictWithLabel(
        data[:, 1, 1], "yright", threshold=threshold
    )

    commandDict = {}
    for mDict in [xLeftPoints, yLeftPoints, xRightPoints, yRightPoints]:
        commandDict.update(mDict)
    commandDict = getContinualMappedNonSympyMergeResult(commandDict)
    commandDictSequential = mergedRangesToSequential(commandDict)

    def getSpanDuration(span):
        start, end = span
        return end - start

    itemDurationThreshold = 10
    # framerate?

    while True:
        # print("LOOP COUNT:", loopCount)
        # loopCount+=1
        # noAlter = True
        beforeChange = [item[0] for item in commandDictSequential].copy()
        for i in range(len(commandDictSequential) - 1):
            currentItem = commandDictSequential[i]
            nextItem = commandDictSequential[i + 1]
            currentItemCommand = currentItem[0]
            currentItemDuration = getSpanDuration(currentItem[1])
            nextItemCommand = nextItem[0]
            nextItemDuration = getSpanDuration(nextItem[1])
            if currentItemDuration < itemDurationThreshold:
                if (
                    nextItemCommand != currentItemCommand
                    and nextItemDuration >= itemDurationThreshold
                ):
                    # print("HERE0",i, currentItemCommand, nextItemCommand)
                    commandDictSequential[i][0] = nextItemCommand
                    # noAlter=False
            if nextItemDuration < itemDurationThreshold:
                if nextItemCommand != currentItemCommand:
                    # print("HERE1",i, currentItemCommand, nextItemCommand)
                    commandDictSequential[i + 1][0] = currentItemCommand
                    # noAlter=False
        afterChange = [item[0] for item in commandDictSequential].copy()
        noAlter = beforeChange == afterChange
        if noAlter:
            break
    preFinalCommandDict = sequentialToMergedRanges(commandDictSequential)
    commandDictSequential = mergedRangesToSequential(preFinalCommandDict)
    if len(commandDictSequential) >= 2:
        _, timespan = commandDictSequential[0]
        nextCommand, nextTimeSpan = commandDictSequential[1]
        currentStart, currentEnd = timespan
        if (currentEnd-currentStart) < 5:
            nextStart, nextEnd = nextTimeSpan
            commandDictSequential[1] = [nextCommand, (currentStart, nextEnd)]
            commandDictSequential.pop(0)
    preFinalCommandDict = sequentialToMergedRanges(commandDictSequential)
    finalCommandDict = {}
    defaultCoords = [int(np.mean(array)) for array in mPoints]
    for key, elem in preFinalCommandDict.items():
        # print(key,elem)
        varNames = ["xleft", "yleft", "xright", "yright"]
        # defaultValues = [0, 0, defaultWidth, defaultHeight]
        defaultValues = defaultCoords
        for varName, defaultValue in zip(varNames, defaultValues):
            key = key.replace(
                "{}:empty".format(varName), "{}:{}".format(
                    varName, defaultValue)
            )
        # print(key,elem)
        # breakpoint()
        import parse

        formatString = (
            "xleft:{xleft:d}|yleft:{yleft:d}|xright:{xright:d}|yright:{yright:d}"
        )
        commandArguments = parse.parse(formatString, key)
        x, y, w, h = (
            commandArguments["xleft"],
            commandArguments["yleft"],
            commandArguments["xright"] - commandArguments["xleft"],
            commandArguments["yright"] - commandArguments["yleft"],
        )
        x += w*(1-shrink)/2
        y += h*(1-shrink)/2
        w *= shrink
        h *= shrink
        x, y, w, h = [int(digit) for digit in (x, y, w, h)]
        if w <= 0 or h <= 0:
            continue
        cropCommand = "crop_{}_{}_{}_{}".format(x, y, w, h)
        # print(cropCommand)
        finalCommandDict.update({cropCommand: elem})
        # print(elem)
        # the parser shall be in x,y,w,h with keywords.
        # we might want to parse the command string and reengineer this shit.
    return finalCommandDict


def kalmanStablePipRegionExporter(data, defaultWidth, defaultHeight, downScale=1, shrink=0.8):
    defaultWidth, defaultHeight = int(defaultWidth), int(defaultHeight)
    import numpy as np

    data = np.array(data)

    def getSinglePointStableState(
        xLeftPoints,
        signalFilterThreshold=10,
        commandFloatMergeThreshold=15,
        stdThreshold=1,
        slopeThreshold=0.2,
        # shrink=0.8
    ):

        xLeftPointsFiltered = Kalman1D(xLeftPoints)
        xLeftPointsFiltered = xLeftPointsFiltered.reshape(-1)
        from itertools import groupby

        def extract_span(mlist, target=0):
            counter = 0
            spanList = []
            target_list = [(a, len(list(b))) for a, b in groupby(mlist)]
            for a, b in target_list:
                nextCounter = counter + b
                if a == target:
                    spanList.append((counter, nextCounter))
                counter = nextCounter
            return spanList

        # solve diff.
        xLeftPointsFilteredDiff = np.diff(xLeftPointsFiltered)
        # xLeftPointsFilteredDiff3 = np.diff(xLeftPointsFilteredDiff)
        # import matplotlib.pyplot as plt
        # plt.plot(xLeftPointsFilteredDiff)
        # plt.plot(xLeftPointsFiltered)
        # plt.plot(xLeftPoints)
        # plt.show()

        # xLeftPointsFilteredDiff3Filtered = Kalman1D(xLeftPointsFilteredDiff3)
        import math
        suggestedDerivativeThreshold = 3*math.sqrt(downScale)
        derivativeThreshold = max(3, suggestedDerivativeThreshold)
        # derivative3Threshold = 3
        xLeftPointsSignal = (
            (abs(xLeftPointsFilteredDiff) < derivativeThreshold)
            .astype(np.uint8)
            .tolist()
        )

        def signalFilter(signal, threshold=10):
            newSignal = np.zeros(len(signal))
            signalFiltered = extract_span(xLeftPointsSignal, target=1)
            newSignalRanges = []
            for start, end in signalFiltered:
                length = end - start
                if length >= threshold:
                    newSignalRanges.append((start, end))
                    newSignal[start: end + 1] = 1
            return newSignal, newSignalRanges

        xLeftPointsSignalFiltered, newSignalRanges = signalFilter(
            xLeftPointsSignal, threshold=signalFilterThreshold
        )
        xLeftPointsSignalFiltered *= 255

        mShrink = 2
        from sklearn.linear_model import LinearRegression

        target = []
        for start, end in newSignalRanges:
            # could we shrink the boundaries?
            mStart, mEnd = start + mShrink, end - mShrink
            if mEnd <= mStart:
                continue
            sample = xLeftPointsFiltered[mStart:mEnd]
            std = np.std(sample)
            if std > stdThreshold:
                continue
            model = LinearRegression()
            X, y = np.array(range(sample.shape[0])).reshape(-1, 1), sample
            model.fit(X, y)
            coef = model.coef_[0]  # careful!
            if abs(coef) > slopeThreshold:
                continue
            meanValue = int(np.mean(sample))
            target.append({"range": (start, end), "mean": meanValue})
            # print((start, end), std, coef)

        newTarget = {}

        for elem in target:
            meanStr = str(elem["mean"])
            mRange = elem["range"]
            newTarget.update({meanStr: newTarget.get(meanStr, []) + [mRange]})

        mStart = 0
        mEnd = len(xLeftPoints)
        newTarget = getContinualMappedNonSympyMergeResultWithRangedEmpty(
            newTarget, mStart, mEnd
        )
        newTargetSequential = mergedRangesToSequential(newTarget)

        if (newTargetSequential) == 1:
            if newTargetSequential[0][0] == "empty":
                # the whole thing is empty now. no need to investigate.
                print("NO STATIC PIP FOUND HERE.")
                return {}
        else:
            # newTargetSequential
            newTargetSequentialUpdated = []
            for index in range(len(newTargetSequential) - 1):
                elem = newTargetSequential[index]
                commandString, commandTimeSpan = elem
                nextElem = newTargetSequential[index + 1]
                nextCommandString, nextCommandTimeSpan = nextElem
                if commandString == "empty":
                    newTargetSequential[index][0] = nextCommandString
                else:
                    if nextCommandString == "empty":
                        newTargetSequential[index + 1][0] = commandString
                    else:  # compare the two!
                        commandFloat = float(commandString)
                        nextCommandFloat = float(nextCommandString)
                        if (
                            abs(commandFloat - nextCommandFloat)
                            < commandFloatMergeThreshold
                        ):
                            newTargetSequential[index + 1][0] = commandString
            # bring this sequential into dict again.
            answer = sequentialToMergedRanges(newTargetSequential)
            # print("_"*30, "ANSWER","_"*30)
            # for elem in answer.items():
            #     print(elem)
            return answer
        print("[FAILSAFE] SOMEHOW THE CODE SUCKS")
        return {}

    xLeftPoints = data[:, 0, 0]
    yLeftPoints = data[:, 0, 1]
    xRightPoints = data[:, 1, 0]
    yRightPoints = data[:, 1, 1]

    mPoints = [xLeftPoints, yLeftPoints, xRightPoints, yRightPoints]

    answers = []
    import math
    suggestedSignalFilterThreshold = int(10*math.sqrt(downScale))
    suggestedStdThreshold = 1*math.sqrt(math.sqrt(downScale))
    suggestedSlopeThreshold = 0.2*math.sqrt(math.sqrt(downScale))
    suggestedCommandFloatMergeThreshold = 15/(math.sqrt(math.sqrt(downScale)))
    for mPoint in mPoints:
        answer = getSinglePointStableState(mPoint, signalFilterThreshold=max(10, suggestedSignalFilterThreshold),
                                           stdThreshold=max(1, suggestedStdThreshold), slopeThreshold=max(0.2, suggestedSlopeThreshold), commandFloatMergeThreshold=max(12, suggestedCommandFloatMergeThreshold))
        answers.append(answer)
        # print("_"*30, "ANSWER","_"*30)
        # for elem in answer.items():
        #     print(elem)
    # breakpoint()
    if answers == [{}, {}, {}, {}]:
        print("NO PIP FOUND")
    #     finalCommandDict = {}
    # else:
    # defaultCoord = [0, 0, defaultWidth, defaultHeight]  # deal with it later?
    defaultCoords = [int(np.mean(array)) for array in mPoints]
    defaults = [{str(defaultCoords[index]): [(0, len(data))]}
                for index in range(4)]
    for index in range(4):
        if answers[index] == {}:
            answers[index] = defaults[index]
    labels = ["xleft", "yleft", "xright", "yright"]
    commandDict = {}
    for index, elem in enumerate(answers):
        label = labels[index]
        newElem = {"{}:{}".format(
            label, key): elem[key] for key in elem.keys()}
        commandDict.update(newElem)
    commandDict = getContinualMappedNonSympyMergeResult(commandDict)
    commandDictSequential = mergedRangesToSequential(commandDict)

    def getSpanDuration(span):
        start, end = span
        return end - start

    itemDurationThreshold = 15
    # print("HERE")
    # loopCount = 0

    while True:
        # print("LOOP COUNT:", loopCount)
        # loopCount+=1
        # noAlter = True
        beforeChange = [item[0] for item in commandDictSequential].copy()
        for i in range(len(commandDictSequential) - 1):
            currentItem = commandDictSequential[i]
            nextItem = commandDictSequential[i + 1]
            currentItemCommand = currentItem[0]
            currentItemDuration = getSpanDuration(currentItem[1])
            nextItemCommand = nextItem[0]
            nextItemDuration = getSpanDuration(nextItem[1])
            if currentItemDuration < itemDurationThreshold:
                if nextItemCommand != currentItemCommand:
                    # print("HERE0",i, currentItemCommand, nextItemCommand)
                    commandDictSequential[i][0] = nextItemCommand
                    # noAlter=False
            if nextItemDuration < itemDurationThreshold:
                if (
                    nextItemCommand != currentItemCommand
                    and currentItemDuration >= itemDurationThreshold
                ):
                    # print("HERE1",i, currentItemCommand, nextItemCommand)
                    commandDictSequential[i + 1][0] = currentItemCommand
                    # noAlter=False
        afterChange = [item[0] for item in commandDictSequential].copy()
        noAlter = beforeChange == afterChange
        if noAlter:
            break
    preFinalCommandDict = sequentialToMergedRanges(commandDictSequential)
    finalCommandDict = {}
    for key, elem in preFinalCommandDict.items():
        # print(key,elem)
        varNames = ["xleft", "yleft", "xright", "yright"]
        # defaultValues = [0, 0, defaultWidth, defaultHeight]
        defaultValues = defaultCoords
        for varName, defaultValue in zip(varNames, defaultValues):
            key = key.replace(
                "{}:empty".format(varName), "{}:{}".format(
                    varName, defaultValue)
            )
        # print(key,elem)
        # breakpoint()
        import parse

        formatString = (
            "xleft:{xleft:d}|yleft:{yleft:d}|xright:{xright:d}|yright:{yright:d}"
        )
        commandArguments = parse.parse(formatString, key)
        x, y, w, h = (
            commandArguments["xleft"],
            commandArguments["yleft"],
            commandArguments["xright"] - commandArguments["xleft"],
            commandArguments["yright"] - commandArguments["yleft"],
        )
        x += w*(1-shrink)/2
        y += h*(1-shrink)/2
        w *= shrink
        h *= shrink
        x, y, w, h = [int(digit) for digit in (x, y, w, h)]
        if w <= 0 or h <= 0:
            continue
        cropCommand = "crop_{}_{}_{}_{}".format(x, y, w, h)
        # print(cropCommand)
        finalCommandDict.update({cropCommand: elem})
        # print(elem)
        # the parser shall be in x,y,w,h with keywords.
        # we might want to parse the command string and reengineer this shit.
    return finalCommandDict


def detectPipRegionOverTime(
    videoPath, start, end, method="framewise", algo="frame_difference", downScale=2, shrink=0.9, minPixelSpan=540
):  # shall be some parameters here.
    # if it is 'skim' we will sample it every 20 frames.
    defaultWidth, defaultHeight = getVideoWidthHeight(videoPath)
    downScale = min(
        (minPixelSpan / min(defaultWidth, defaultHeight)), downScale)
    import pybgs as bgs

    assert algo in ["frame_difference", "weighted_moving_average"]
    if algo == "frame_difference":
        algorithm = bgs.FrameDifference()
        # much faster.
    else:
        algorithm = bgs.WeightedMovingAverage()
        # slower. don't know if it works or not.
        # it does produce different results.
    # otherwise we do it frame by frame.
    assert method in ["skim", "framewise"]
    pipFrames = []
    # batch= 1
    if method == "framewise":
        sample_rate = 1
        batch = 1
    else:
        # batch = 4
        batch = 2
        videoFrameRate = getVideoFrameRate(videoPath)
        totalFramesInSegment = (end - start) * videoFrameRate
        minSampleSize = int((80*4)*(totalFramesInSegment/1800))
        min_sample_rate = int(totalFramesInSegment / minSampleSize)
        estimated_sample_rate = min(5, min_sample_rate)
        sample_rate = max(1, estimated_sample_rate)
    iterator = getVideoFrameIterator(
        videoPath, start, end, sample_rate=sample_rate, batch=batch)
    areaThreshold = int(0.2 * 0.2 * defaultWidth * defaultHeight)
    pipFrames = []
    defaultRect = [(0, 0), (defaultWidth, defaultHeight)]

    for index, frame in enumerate(iterator):
        # for _ in range(downScale):
        downScaledFrame = cv2.resize(
            frame, (int(defaultWidth/downScale), int(defaultHeight/downScale)))
        img_output = algorithm.apply(downScaledFrame)
        if batch != 1 and index % batch == 0:
            continue
        if batch == 1 and index == 0:
            continue
        [x, y, w, h] = cv2.boundingRect(img_output)  # wtf is this?
        x, y, w, h = x*downScale, y*downScale, w*downScale, h*downScale
        area = w * h
        if area > areaThreshold:
            min_x, min_y = x, y
            max_x, max_y = x + w, y + h
            currentRect = [(min_x, min_y), (max_x, max_y)]
            pipFrames.append(currentRect.copy())
            defaultRect = currentRect.copy()
        else:
            pipFrames.append(defaultRect.copy())
    # now finished collecting shit... need to convert it to something readable.
    sampleLength = len(pipFrames)
    clipDuration = end - start
    sampleIndexToSecondsRatio = clipDuration / sampleLength
    if method == "framewise":
        resultDict = kalmanStablePipRegionExporter(
            pipFrames, defaultWidth, defaultHeight, downScale=downScale, shrink=shrink
        )
    else:
        resultDict = sampledStablePipRegionExporter(
            pipFrames, defaultWidth, defaultHeight, shrink=shrink
        )
    finalResultDict = {}
    for key, value in resultDict.items():
        updatedValueAlignedToSeconds = []
        for mStart, mEnd in value:
            mStart = start+mStart*sampleIndexToSecondsRatio
            mEnd = start+mEnd*sampleIndexToSecondsRatio
            mStart = max(start, mStart)
            mEnd = min(end, mEnd)
            mDuration = mEnd-mStart
            if mDuration <= 0:
                continue
            updatedValueAlignedToSeconds.append((mStart, mEnd))
        finalResultDict.update({key: updatedValueAlignedToSeconds.copy()})
    return finalResultDict
