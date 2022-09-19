# funny sight.
# we plan to put automatic watermark detection here. no issue?
# import numpy as np
from pyjom.commons import *
from pyjom.mathlib import *
import cv2
from pyjom.imagetoolbox import *
from functools import lru_cache

def dummyFilterFunction(report:bool, *args, **kwargs): return report
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
        w = math.floor(w / 2) * 2
        if w <= 2:
            return False, None
    if y + h >= height:
        h = height - y - 1
        h = math.floor(h / 2) * 2
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
    if startFrame <= 0:
        startFrame = 0
    stopFrame = int(end * fps)
    if stopFrame <= 0:
        stopFrame = total_frames
    if stopFrame <= startFrame:
        print("some fuck is going on with the video frame sampler")
        breakpoint()
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


def getVideoFrameIterator(
    videoPath,
    start,
    end,
    sample_rate: float = 1,
    batch: int = 1,
    screenshot=False,
    epsilon=0.00000001,
):
    if screenshot:
        end = start + epsilon
    assert batch >= 1
    assert sample_rate > 0  # this might not work for those<1 ones. really?
    # assert end>start
    cap = cv2.VideoCapture(videoPath)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    if start >= 0:
        startFrame = int(start * fps)
    else:
        startFrame = 0
    if end > start and end > 0:
        endFrame = int(end * fps)
    else:
        endFrame = total_frames

    startFrame = min(max(0, startFrame), total_frames - 1)
    endFrame = max(1, min(total_frames, endFrame), startFrame + 1)
    # success, img = cap.read() # ignore first frame.
    # https://vuamitom.github.io/2019/12/13/fast-iterate-through-video-frames.html
    # to speed up the process we need to decompose the cap.read() method
    # and even better:
    # the official provides multithreading support. no thanks?
    import progressbar

    # replace it with linspace.
    import numpy as np

    linspace = np.linspace(
        startFrame, endFrame, int((endFrame - startFrame) / sample_rate) + 1
    )

    for fno in progressbar.progressbar(linspace):
        # for fno in progressbar.progressbar(range(startFrame, stopFrame + 1, sample_rate)):
        fno = int(fno)
        fnoMax = fno + batch - 1
        if fnoMax >= total_frames:
            break
        for fnoX in range(batch):
            cap.set(cv2.CAP_PROP_POS_FRAMES, fnoX + fno)
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


def getVideoFrameIteratorWithFPS(videoPath, start: float, end: float, fps=1):
    # this will set batch to 1
    from caer.video.frames_and_fps import get_fps_float

    source_fps = get_fps_float(videoPath)
    sample_rate = source_fps / fps
    return getVideoFrameIterator(videoPath, start, end, sample_rate=sample_rate)


def getDiagonalRectArea(diagonalRect):
    (x0, y0), (x1, y1) = diagonalRect
    area = (x1 - x0) * (y1 - y0)
    return area


@lru_cache(maxsize=20)
def detectTextRegionOverTime(
    videoPath,
    start,
    end,
    sample_rate=3,
    mergeThreshold=10,
    langs: list = ["en"],
    top_k=10,
):  # this sample rate is too unreasonable. set it to 3 or something.
    iterator = getVideoFrameIterator(videoPath, start, end, sample_rate=sample_rate)
    detectionList = []
    # use some merging technique over time.
    # convolution?
    import easyocr

    # no metal? no dbnet18?
    reader = easyocr.Reader(langs, gpu=True, recognizer=False)
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
        if top_k > 0:
            mergedRects.sort(
                key=lambda diagonalRect: -getDiagonalRectArea(diagonalRect)
            )  # this is diagonal.
            mergedRects = mergedRects[:top_k]
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

    def getRounded(num, rounder):
        return (num // rounder) * rounder

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


@lru_cache(maxsize=30)
def detectStationaryLogoOverTime(
    filepath,
    start,
    end,
    sample_size=60,
    cornersOnly=True,
    pipCropDicts=None,
    areaThreshold=30,
    top_k: int = 0,
):
    top_k = int(top_k)
    imageSet = getVideoFrameSampler(filepath, start, end, sample_size=sample_size)
    # what is this src?
    # from src import *
    defaultWidth, defaultHeight = getVideoWidthHeight(filepath)

    def getDeltaWidthHeight(defaultWidth, defaultHeight):
        deltaWidthRatio = 4 + (4 - 3) * (defaultWidth / defaultHeight - 16 / 9) / (
            16 / 9 - 9 / 16
        )
        deltaWidthRatio = makeValueInRange(deltaWidthRatio, 3, 4)
        deltaHeightRatio = 8 + (8 - 6) * (defaultHeight / defaultWidth - 16 / 9) / (
            16 / 9 - 9 / 16
        )
        deltaHeightRatio = makeValueInRange(deltaHeightRatio, 6, 8)
        deltaWidth, deltaHeight = int(defaultWidth / deltaWidthRatio), int(
            defaultHeight / deltaHeightRatio
        )
        return deltaWidth, deltaHeight

    def getFourCorners(x, y, defaultWidth, defaultHeight):
        deltaWidth, deltaHeight = getDeltaWidthHeight(defaultWidth, defaultHeight)
        # (x1, y1), (x2, y2)
        fourCorners = [
            [(0, 0), (deltaWidth, deltaHeight)],
            [(defaultWidth - deltaWidth, 0), (defaultWidth, deltaHeight)],
            [
                (defaultWidth - deltaWidth, defaultHeight - deltaHeight),
                (defaultWidth, defaultHeight),
            ],
            [(0, defaultHeight - deltaHeight), (deltaWidth, defaultHeight)],
        ]
        fourCorners = [
            [(a + x, b + y), (c + x, d + y)] for [(a, b), (c, d)] in fourCorners
        ]
        return fourCorners

    fourCorners = None
    from functools import reduce

    cornerArea = reduce(
        lambda x, y: x * y, getDeltaWidthHeight(defaultWidth, defaultHeight)
    )
    if cornersOnly:
        defaultFourCorners = getFourCorners(0, 0, defaultWidth, defaultHeight)
        if pipCropDicts in [None, {}]:
            fourCorners = defaultFourCorners
        else:
            from pyjom.mathlib import (
                getContinualMappedNonSympyMergeResultWithRangedEmpty,
            )

            pipCropDictsWithRangedEmpty = (
                getContinualMappedNonSympyMergeResultWithRangedEmpty(
                    pipCropDicts, start, end
                )
            )
            # pipCropDictsWithRangedEmptySequential = mergedRangesToSequential(pipCropDictsWithRangedEmpty) # this is not needed. maybe?
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
    W_full = (W_full - minval) * (255 / (maxval - minval))  # is that necessary?
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
    boundingRects = []
    for cnt in cnts2:
        x, y, w, h = cv2.boundingRect(cnt)  # Draw the bounding box image
        currentRect = [(x, y), (x + w, y + h)]
        boundingRects.append(currentRect.copy())
    print("TOTAL {} STATIONARY LOGOS.".format(len(cnts2)))
    delogoCommandList = []  # test if it can merge anything!
    if (fourCorners is not None) or (not cornersOnly):
        start_end_ranges = [(start, end)]
        start_end_list = [[None, start_end_ranges]]
    else:
        start_end_list = []
        for crop_flag, start_end_ranges in pipCropDictsWithRangedEmpty.items():
            if crop_flag == "empty":
                crop_flag = None
            start_end_list.append([crop_flag, start_end_ranges])

    def getTopKCandidates(sortedList, top_k):
        if top_k <= 0:
            return sortedList
        else:
            return sortedList[:top_k]

    for index, (crop_flag, start_end_ranges) in enumerate(start_end_list):
        # for mStart, mEnd in start_end_ranges:
        mFinalDelogoFilters = []
        if top_k > 0:
            boundingRects.sort(
                key=lambda rect: abs(
                    (rect[1][0] - rect[0][0]) * (rect[1][1] - rect[0][1]) - cornerArea
                )
            )
            boundingRects = getTopKCandidates(boundingRects, top_k)

        for currentRect in boundingRects:
            if cornersOnly:
                if crop_flag is None:
                    currentFourCorners = defaultFourCorners
                else:
                    import parse

                    parseResult = parse.parse("crop_{x}_{y}_{w}_{h}", crop_flag)
                    currentFourCorners = getFourCorners(
                        parseResult["x"],
                        parseResult["y"],
                        parseResult["w"],
                        parseResult["h"],
                    )
                    for cornerRect in currentFourCorners:
                        overlapRect = getOverlapRect(currentRect, cornerRect)
                        if overlapRect:
                            (x0, y0), (x1, y1) = overlapRect
                            x, y, w, h = x0, y0, x1 - x0, y1 - y0
                            area = w * h
                            if area < areaThreshold:
                                continue
                            delogoCommand = "delogo_{}_{}_{}_{}".format(x, y, w, h)
                            # print(delogoCommand)
                            # print('width:{} height:{}'.format(b,a))
                            mFinalDelogoFilters.append(delogoCommand)
            else:
                [(x, y), (x_w, y_h)] = currentRect
                w = x_w - x
                h = y_h - y
                area = w * h
                if area < areaThreshold:
                    continue
                delogoCommand = "delogo_{}_{}_{}_{}".format(x, y, w, h)
                mFinalDelogoFilters.append(delogoCommand)
            # cv2.rectangle(output, (x,y), (x+w,y+h), (0,0,255),2)
            # cv2.rectangle(myMask2, (x, y), (x + w, y + h), 255, -1)
        # get the final dictionary
        if len(mFinalDelogoFilters) == 0:
            values = [{}]
        else:
            delogoCommandSet = "|".join(mFinalDelogoFilters)
            values = []
            for (mStart, mEnd) in start_end_ranges:
                values.append(
                    {delogoCommandSet: (mStart, mEnd)}
                )  # can it be turned into something useful?
        delogoCommandList.extend(values)  # this is a sequential list.
    from pyjom.mathlib import sequentialToMergedRanges

    delogoCommandDict = sequentialToMergedRanges(delogoCommandList)

    return delogoCommandDict  # is this freaking sequential? no?


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
            resultDict.update({mKey: resultDict.get(mKey, []) + [(index, index + 1)]})
        return resultDict

    def pointsToRangedDictWithLabel(mArray, label, threshold=35, method="kalman"):
        assert method in ["ema", "kalman"]
        if method == "ema":
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
        if (currentEnd - currentStart) < 5:
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
                "{}:empty".format(varName), "{}:{}".format(varName, defaultValue)
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
        x += w * (1 - shrink) / 2
        y += h * (1 - shrink) / 2
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


def kalmanStablePipRegionExporter(
    data, defaultWidth, defaultHeight, downScale=1, shrink=0.8
):
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

        suggestedDerivativeThreshold = 3 * math.sqrt(downScale)
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
                    newSignal[start : end + 1] = 1
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

    suggestedSignalFilterThreshold = int(10 * math.sqrt(downScale))
    suggestedStdThreshold = 1 * math.sqrt(math.sqrt(downScale))
    suggestedSlopeThreshold = 0.2 * math.sqrt(math.sqrt(downScale))
    suggestedCommandFloatMergeThreshold = 15 / (math.sqrt(math.sqrt(downScale)))
    for mPoint in mPoints:
        answer = getSinglePointStableState(
            mPoint,
            signalFilterThreshold=max(10, suggestedSignalFilterThreshold),
            stdThreshold=max(1, suggestedStdThreshold),
            slopeThreshold=max(0.2, suggestedSlopeThreshold),
            commandFloatMergeThreshold=max(12, suggestedCommandFloatMergeThreshold),
        )
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
    defaults = [{str(defaultCoords[index]): [(0, len(data))]} for index in range(4)]
    for index in range(4):
        if answers[index] == {}:
            answers[index] = defaults[index]
    labels = ["xleft", "yleft", "xright", "yright"]
    commandDict = {}
    for index, elem in enumerate(answers):
        label = labels[index]
        newElem = {"{}:{}".format(label, key): elem[key] for key in elem.keys()}
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
                "{}:empty".format(varName), "{}:{}".format(varName, defaultValue)
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
        x += w * (1 - shrink) / 2
        y += h * (1 - shrink) / 2
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


@lru_cache(maxsize=20)
def detectPipRegionOverTime(
    videoPath,
    start,
    end,
    method="framewise",
    algo="frame_difference",
    downScale=2,
    shrink=0.9,
    minPixelSpan=540,
):  # shall be some parameters here.
    # if it is 'skim' we will sample it every 20 frames.
    defaultWidth, defaultHeight = getVideoWidthHeight(videoPath)
    downScale = min((minPixelSpan / min(defaultWidth, defaultHeight)), downScale)
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
        minSampleSize = int((80 * 4) * (totalFramesInSegment / 1800))
        min_sample_rate = int(totalFramesInSegment / minSampleSize)
        estimated_sample_rate = min(5, min_sample_rate)
        sample_rate = max(1, estimated_sample_rate)
    iterator = getVideoFrameIterator(
        videoPath, start, end, sample_rate=sample_rate, batch=batch
    )
    areaThreshold = int(0.2 * 0.2 * defaultWidth * defaultHeight)
    pipFrames = []
    defaultRect = [(0, 0), (defaultWidth, defaultHeight)]

    for index, frame in enumerate(iterator):
        # for _ in range(downScale):
        downScaledFrame = cv2.resize(
            frame, (int(defaultWidth / downScale), int(defaultHeight / downScale))
        )
        img_output = algorithm.apply(downScaledFrame)
        if batch != 1 and index % batch == 0:
            continue
        if batch == 1 and index == 0:
            continue
        [x, y, w, h] = cv2.boundingRect(img_output)  # wtf is this?
        x, y, w, h = x * downScale, y * downScale, w * downScale, h * downScale
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
            mStart = start + mStart * sampleIndexToSecondsRatio
            mEnd = start + mEnd * sampleIndexToSecondsRatio
            mStart = max(start, mStart)
            mEnd = min(end, mEnd)
            mDuration = mEnd - mStart
            if mDuration <= 0:
                continue
            updatedValueAlignedToSeconds.append((mStart, mEnd))
        finalResultDict.update({key: updatedValueAlignedToSeconds.copy()})
    return finalResultDict


from lazero.filesystem import tmpdir
from typing import Literal


def getEffectiveFPS(
    videoPath,
    tempdir="/dev/shm/medialang/get_effective_fps",
    conversionFPS=15,
    debug=False,
    mpdecimate_args_choice: Literal[
        None, "hi=1:lo=1:frac=1:max=0", "hi=200:lo=200:frac=1:max=0"
    ] = None,
):
    # use ffmpeg to covert the target first!
    import uuid
    import os

    tempdir = os.path.join(tempdir, str(uuid.uuid4()))
    # changed so we can wipe this thing out.

    with tmpdir(path=tempdir) as tempDirObj:
        ####################
        #!/usr/bin/env python3

        import sys
        import time
        from functools import partial
        from subprocess import run
        from typing import Union

        # this shit is ridiculus.
        from pyjom.commons import ffprobe_media_info, extract_span

        def wrapperFunc(function, *args, **kwargs):
            stdout = sys.stdout
            sys.stdout = sys.stderr  # wtf is this shit?
            try:
                return function(*args, **kwargs)
            except:
                import traceback

                traceback.print_exc()
                print("Error when executing mpdecimate function")
            sys.stdout = stdout

        def mpdecimate_export_duplicate_clip_ranges_base(
            filepath: str = None,
            mpdecimate_args: Union[None, str] = "hi=576",
            video_size: Union[None, str] = None,
        ):
            flag_vaapi = False  # not using vaapi.
            flag_vaapi_decimate = False
            videoDuration = None
            try:
                from caer.video.frames_and_fps import get_duration

                duration = get_duration(videoPath)
            except:
                import traceback

                traceback.print_exc()
                print("error when getting video duration by caer")
            if videoDuration is None:
                from MediaInfo import MediaInfo

                info = MediaInfo(filename=filepath).getInfo()
                # cannot get shit from this.
                # print(info.keys())
                # breakpoint()
                videoDuration = None
                if type(info) == dict:
                    videoDuration = info.get(
                        "videoDuration", info.get("duration", None)
                    )
                if videoDuration is not None:
                    videoDuration = float(videoDuration)
                else:
                    info = ffprobe_media_info(filepath, video_size=video_size)
                    try:
                        videoDuration = info["streams"][0][
                            "duration"
                        ]  # sure it is gif.
                    except:
                        import traceback

                        traceback.print_exc()
                        print("Video duration not acquired.")
                        print(info)
                        breakpoint()
            print("video duration:", [videoDuration])

            def prof(s):
                e = time.time()
                print("Taken time:", time.strftime("%H:%M:%S", time.gmtime(e - s)))
                return e

            def profd(f):
                def a(*args, **kwargs):
                    s = time.time()
                    r = f(*args, **kwargs)
                    prof(s)
                    return r

                return a

            _hwargs = ["-hwaccel", "vaapi", "-hwaccel_device"]

            def hwargs_decimate():
                # actually input args.
                if video_size:
                    return ["-video_size", video_size]
                return []

            def hwargs_transcode():
                return (
                    [*_hwargs, flag_vaapi, "-hwaccel_output_format", "vaapi"]
                    if flag_vaapi
                    else []
                )

            def _ffmpeg(fi, co, *args, hwargs=[]):
                args = ["ffmpeg", *hwargs, "-i", fi, *args]
                result = run(args, check=not co, capture_output=co)
                if result.returncode == 0:
                    return result

                print(f"Command {args} failed with code {result.returncode}")
                print("--------    STDOUT S    --------")
                print(result.stdout.decode())
                print("--------    STDOUT E    --------")
                print("--------    STDERR S    --------")
                print(result.stderr.decode())
                print("--------    STDERR E    --------")
                sys.exit(3)

            ffmpeg = profd(partial(_ffmpeg, filepath))

            def trim(s, e, i, b1=b"v", b2=b""):
                # if e is None, it indicates end matchs the clip's end
                trim = b"%f:%f" % (s, e) if e is not None else b"%f" % s
                return b"[0:%b]%btrim=%b,%bsetpts=PTS-STARTPTS[%b%d];" % (
                    b1,
                    b2,
                    trim,
                    b2,
                    b1,
                    i,
                )  # presetation timestamp trick

            atrim = partial(trim, b1=b"a", b2=b"a")

            def get_dframes(mpdecimate):
                dframes = []
                mList = []
                for line in mpdecimate.split(b"\n"):
                    lineDecoded = line.decode("utf-8").replace("\n", "")
                    if lineDecoded.startswith("[Parsed_mpdecimate"):
                        coreInfo = "SHIT" + lineDecoded.split("]")[-1]
                        import parse

                        mFormat = "{} {flag:l} pts:{pts:g} pts_time:{pts_time:g} drop_count:{drop_count:g}"
                        result = parse.parse(mFormat, coreInfo)
                        # print(coreInfo)
                        # print(result)
                        # breakpoint()
                        if result is not None:
                            pts_time = result["pts_time"]
                            flag = result["flag"]
                            if pts_time > videoDuration:
                                if mList[-1][1] != videoDuration:
                                    flag = mList[-1][0]
                                    pts_time = videoDuration
                                else:
                                    break
                            mResult = flag, pts_time
                            mList.append(mResult)
                # mList = [(flag, pts_time), ...]
                mList.sort(key=lambda x: x[1])
                binarizedRange = [0 if x[0] == "keep" else 1 for x in mList]
                # so we select all the ones.
                spans = extract_span(binarizedRange, target=1)
                for start, end in spans:
                    end -= 1  # crucial. allow jerk moves
                    if start >= end:
                        print("START", start, "END", end)
                        print("________WTF IS GOING ON________")
                        continue  # we don't need this shit.
                    start_timestamp, end_timestamp = mList[start][1], mList[end][1]
                    dframes.append((start_timestamp, end_timestamp))
                # print(binarizedRange)
                # print(dframes)
                # print(spans)
                # breakpoint()
                return dframes, (binarizedRange, mList, spans)

            ### this is the dframes detection part.

            mpdecimate = ffmpeg(
                True,
                "-vf",
                "mpdecimate={}".format(mpdecimate_args)
                if mpdecimate_args
                else "mpdecimate",  # here to set the threshold.
                "-loglevel",
                "debug",
                "-f",
                "null",
                "-",
                hwargs=hwargs_decimate(),
            ).stderr
            dframes2, (binarizedRange, mList, spans) = get_dframes(mpdecimate)

            ### this is the dframes detection part.
            dupDuration = sum([end - start for start, end in dframes2])
            dupPercent = dupDuration / videoDuration  # type: ignore
            frameDupPercent = sum(binarizedRange) / len(binarizedRange)
            return dframes2, dupPercent, frameDupPercent, (binarizedRange, mList, spans)

        def mpdecimate_export_duplicate_clip_ranges(
            filepath: str = None,
            mpdecimate_args: Union[None, str] = "hi=576",
            video_size: Union[None, str] = None,
        ):
            return wrapperFunc(
                mpdecimate_export_duplicate_clip_ranges_base,
                filepath=filepath,
                mpdecimate_args=mpdecimate_args,
                video_size=video_size,
            )

        # source = "/root/Desktop/works/pyjom/samples/video/nearly_duplicate_frames_detection.gif"

        # source = "/root/Desktop/works/pyjom/samples/video/nearly_duplicate_frames_detection_30fps.rgb"
        # source = "/root/Desktop/works/pyjom/samples/video/nearly_duplicate_frames_detection_30fps_blend.mp4"

        # source = "/root/Desktop/works/pyjom/samples/video/kitty_flash.gif" # 9.50 fps freaking hell.
        # how about 15fps or something
        import uuid
        import os

        convertedVideoPath = str(uuid.uuid4()) + ".mp4"
        convertedVideoPath = os.path.join(tempdir, convertedVideoPath)

        commandline = "ffmpeg -y -i {} -vf minterpolate=fps={}:mi_mode=dup {}".format(
            videoPath, conversionFPS, convertedVideoPath
        )
        commandArgs = commandline.split(" ")
        print("converting video file to {}fps mp4".format(conversionFPS))
        # os.system(commandline)
        output = subprocess.check_output(commandArgs)
        # will raise error if conversion failed.
        print(output)
        print("convertion done")

        source = convertedVideoPath  # very unlikely to go higher.
        # 15fps is just fine for shit like this.
        # source = "/root/Desktop/works/pyjom/samples/video/kitty_flash.mp4" # very unlikely to go higher.

        # source = "/root/Desktop/works/pyjom/samples/video/nearly_duplicate_frames_detection_30fps.mp4"
        # source = "/root/Desktop/works/pyjom/samples/video/nearly_duplicate_frames_detection_30fps.gif"
        # source = "/root/Desktop/works/pyjom/samples/video/nearly_duplicate_frames_detection.mp4"
        # videoDuration, duration
        # source = "/root/Desktop/works/pyjom/samples/video/dog_with_text.mp4" # what about this?
        # shit. wtf is going on?
        # now it is good. no reply for dog_with_text.mp4 with strictest settings.

        result = mpdecimate_export_duplicate_clip_ranges(
            source,
            mpdecimate_args=mpdecimate_args_choice
            # ,video_size="480x480"
        )

        # turned out mp4 encoded video actually outperforms original gif.

        # ffmpeg's libx264 is good. gif shit is bad. don't know what happens out there. :)

        # use 'blend' instead of 'dup'

        if result is not None:
            (
                dframes2,
                dupPercent,
                frameDupPercent,
                (binarizedRange, mList, spans),
            ) = result
            for i, (s, e) in enumerate(dframes2):
                # start, end.
                print("INDEX", i, "START", s, "END", e)
            print("DUPLICATE PERCENTAGE: {:.2f} %".format(dupPercent * 100))
            print("FRAME DUPLICATE PERCENTAGE: {:.2f} %".format(frameDupPercent * 100))
            effectiveFPS = (1 - frameDupPercent) * conversionFPS
            debugInfo = {
                "binarized_frame_keep_drop_flags": binarizedRange,
                "frame_list_with_pts_and_flag": mList,
                "drop_frame_index_spans": spans,
            }
            print("EFFECTIVE FPS: {:.2f}".format(effectiveFPS))
        else:
            print("dframes2 is None")
            effectiveFPS = conversionFPS
            dupPercent = frameDupPercent = 0
            dframes2 = []
            debugInfo = None
        ####################
        if debug:
            return {
                "duplicatePercent": dupPercent,
                "frameDuplicatePercent": frameDupPercent,
                "effectiveFPS": effectiveFPS,
                "duplicatedFrameRanges": dframes2,
                "debugInfo": debugInfo,
            }  # time ranges of duplicated frames
        else:
            return effectiveFPS


# this is a generator, not a list!
def getVideoColorCentrality(videoPath, denoise=True, frame_sample_limit=3, **kwargs):
    videoFrameSampler = getVideoFrameSampler(videoPath, -1, -1, frame_sample_limit)
    print("testing video color centrality")
    import progressbar

    for frame in progressbar.progressbar(videoFrameSampler):
        if denoise:
            frame = imageDenoise(frame)
        centrality, max_nearby_center_percentage = getImageColorCentrality(
            frame, **kwargs
        )
        yield centrality, max_nearby_center_percentage


def checkVideoColorCentrality(
    videoColorCentralityGenerator,
    video_color_filter: dict = {
        "centrality": {"max": 0.06},
        "max_nearby_center_percentage": {"max": 0.05},
    },
):
    for centrality, max_nearby_center_percentage in videoColorCentralityGenerator:
        d_a = video_color_filter.get("centrality", {})
        d_b = video_color_filter.get("max_nearby_center_percentage", {})
        a = checkMinMaxDict(centrality, d_a)
        b = checkMinMaxDict(
            max_nearby_center_percentage,
            d_b,
        )
        # print("DICT A", d_a)
        # print("DICT B", d_b)
        # print("FLAG A", a, "FLAG B", b)
        # breakpoint()
        flag = a and b
        if not flag:
            return False
    return True


########################### DOG CAT DETECTION #########################
from pyjom.modules.contentReviewer import filesystemReviewer
from pyjom.commons import keywordDecorator
from lazero.utils.logger import sprint

from pyjom.mathlib import superMean, superMax

import paddlehub as hub
from functools import lru_cache


def extractYolov5DetectionData(detectionData, mimetype="video", debug=False):
    # plan to get some calculations!
    filepath, review_data = detectionData["review"]["review"]
    timeseries_data = review_data["yolov5_detector"]["yolov5"]["yolov5_detector"]
    data_dict = {}
    if mimetype == "video":
        dataList = []
        for frameData in timeseries_data:
            timestamp, frameNumber, frameDetectionData = [
                frameData[key] for key in ["time", "frame", "yolov5_detector"]
            ]
            if debug:
                sprint("timestamp:", timestamp)
            current_shot_detections = []
            for elem in frameDetectionData:
                location, confidence, identity = [
                    elem[key] for key in ["location", "confidence", "identity"]
                ]
                identity = identity["name"]
                if debug:
                    print("location:", location)
                    print("confidence:", confidence)
                    sprint(
                        "identity:", identity
                    )  # we should use the identity name, instead of the identity dict, which is the original identity object.
                current_shot_detections.append(
                    {
                        "location": location,
                        "confidence": confidence,
                        "identity": identity,
                    }
                )
            dataList.append(
                {"timestamp": timestamp, "detections": current_shot_detections}
            )
        data_dict.update({"data": dataList})
    else:
        frameDetectionData = timeseries_data
        current_shot_detections = []
        for elem in frameDetectionData:
            location, confidence, identity = [
                elem[key] for key in ["location", "confidence", "identity"]
            ]
            identity = identity["name"]
            if debug:
                print("location:", location)
                print("confidence:", confidence)
                sprint("identity:", identity)
        data_dict.update(
            {"data": current_shot_detections}
        )  # just detections, not a list in time series order
    data_dict.update({"path": filepath, "type": mimetype})
    return data_dict


def calculateVideoMaxDetectionConfidence(
    dataList, identities=["dog", "cat"]
):  # does it have a dog?
    report = {identity: 0 for identity in identities}
    for elem in dataList:
        detections = elem["detections"]
        for detection in detections:
            identity = detection["identity"]
            if identity in identities:
                if report[identity] < detection["confidence"]:
                    report[identity] = detection["confidence"]
    return report


from typing import Literal
import numpy as np


def calculateVideoMeanDetectionConfidence(
    dataList: list,
    identities=["dog", "cat"],
    framewise_strategy: Literal["mean", "max"] = "max",
    timespan_strategy: Literal["max", "mean", "mean_no_missing"] = "mean_no_missing",
):
    report = {identity: [] for identity in identities}
    # report = {}
    for elem in dataList:  # iterate through selected frames
        # sprint("ELEM")
        # sprint(elem)
        # breakpoint()
        detections = elem["detections"]
        frame_detection_dict_source = {}
        # frame_detection_dict = {key:[] for key in identities}
        for (
            detection
        ) in detections:  # in the same frame, iterate through different detections
            identity = detection["identity"]
            if identity in identities:
                frame_detection_dict_source[identity] = frame_detection_dict_source.get(
                    identity, []
                ) + [detection["confidence"]]
        frame_detection_dict = {}
        for key in identities:
            valueList = frame_detection_dict_source.get(key, [0])
            if framewise_strategy == "mean":
                frame_detection_dict.update({key: superMean(valueList)})
            elif framewise_strategy == "max":
                frame_detection_dict.update({key: superMax(valueList)})
        # now update the report dict.
        for identity in identities:
            value = frame_detection_dict.get(identity, 0)
            if timespan_strategy == "mean_no_missing":
                if value == 0:
                    continue
            report[identity].append(value)
    final_report = {}
    for identity in identities:
        valueList = report.get(identity, [0])
        if timespan_strategy in ["mean_no_missing", "mean"]:
            final_report[identity] = superMean(valueList)
        else:
            final_report[identity] = superMax(valueList)
    return final_report


from pyjom.commons import checkMinMaxDict


def detectionConfidenceFilter(
    detectionConfidence: dict,
    filter_dict={
        "dog": {"min": 0.5},
        "cat": {"min": 0.5},
    },  # both have certainty of 0.69 or something. consider to change this value higher?
    logic: Literal["AND", "OR"] = "OR",
):  # what is the logic here? and? or?
    assert logic in ["AND", "OR"]
    for identity in filter_dict.keys():
        value = detectionConfidence.get(identity, 0)
        key_filter = filter_dict[identity]
        result = checkMinMaxDict(value, key_filter)
        if result:
            if logic == "OR":
                return True
        else:
            if logic == "AND":
                return False
    if logic == "AND":
        return True  # for 'AND' this will be True, but for 'OR' this will be False
    elif logic == "OR":
        return False
    else:
        raise Exception("Invalid logic: %s" % logic)


def yolov5VideoDogCatDetector(
    videoPath,
    debug=False,
    filter_dict={
        "dog": {"min": 0.5},
        "cat": {"min": 0.5},
    },
    logic: Literal["AND", "OR"] = "OR",
):

    autoArgs = {
        "subtitle_detector": {"timestep": 0.2},
        "yolov5_detector": {"model": "yolov5x"},  # will this run? no OOM?
    }  # threshold: 0.4

    template_names = ["yolov5_detector.mdl.j2"]
    semiauto = False
    dummy_auto = False

    reviewer = keywordDecorator(
        filesystemReviewer,
        auto=True,
        semiauto=semiauto,
        dummy_auto=dummy_auto,
        template_names=template_names,
        args={"autoArgs": autoArgs},
    )
    # videoPath = "/root/Desktop/works/pyjom/samples/image/dog_with_text2.png"
    # fileList = [{"type": "image", "path": videoPath}]

    fileList = [{"type": "video", "path": videoPath}]
    # fileList = [{"type": "video", "path": videoPath} for videoPath in videoPaths]

    # resultGenerator, function_id = reviewer(
    #     fileList, generator=True, debug=False
    # )  # or at least a generator?

    resultList, function_id = reviewer(
        fileList, generator=False, debug=False
    )  # or at least a generator?
    result = resultList[0]

    detectionData = extractYolov5DetectionData(result, mimetype=fileList[0]["type"])
    # sprint("DETECTION DATA:")
    # sprint(detectionData)
    filepath = detectionData["path"]
    if debug:
        sprint("FILEPATH: %s" % filepath)
    filetype = detectionData["type"]
    dataList = detectionData["data"]
    detectionConfidence = calculateVideoMeanDetectionConfidence(dataList)
    if debug:
        sprint("DETECTION CONFIDENCE:", detectionConfidence)
    filter_result = detectionConfidenceFilter(
        detectionConfidence, filter_dict=filter_dict, logic=logic
    )
    return filter_result


import paddlehub as hub
from functools import lru_cache


@lru_cache(maxsize=1)
def getPaddleResnet50AnimalsClassifier():
    classifier = hub.Module(name="resnet50_vd_animals")
    return classifier


@lru_cache(maxsize=3)
def labelFileReader(filename):
    with open(filename, "r") as f:
        content = f.read()
        content = content.split("\n")
        content = [elem.replace("\n", "").strip() for elem in content]
        content = [elem for elem in content if len(elem) > 0]
    return content


from pyjom.mathlib import multiParameterExponentialNetwork

# {'input_bias': 0.0830047243746045, 'skew': -0.4986098769473948}
def bezierPaddleHubResnet50VideoDogCatDetector(
    videoPath,
    input_bias=0.0830047243746045,
    skew=-0.4986098769473948,
    threshold=0.5,
    dog_label_file_path="/root/Desktop/works/pyjom/tests/animals_paddlehub_classification_resnet/dogs.txt",
    cat_label_file_path="/root/Desktop/works/pyjom/tests/animals_paddlehub_classification_resnet/cats.txt",
    debug=False,
    logic: Literal["AND", "OR"] = "OR",
):
    filter_dict = {
        "dog": {"min": threshold},
        "cat": {"min": threshold},
    }
    curve_function_kwargs = {
        "start": (0, 0),
        "end": (1, 1),
        "skew": skew,
    }  # maximize the output.
    from pyjom.videotoolbox import getVideoFrameIteratorWithFPS
    from pyjom.imagetoolbox import resizeImageWithPadding

    dog_suffixs = ["狗", "犬", "梗"]
    cat_suffixs = ["猫"]  # ends with this, and not containing forbidden words.
    dog_labels = labelFileReader(dog_label_file_path)
    cat_labels = labelFileReader(cat_label_file_path)

    forbidden_words = [
        "灵猫",
        "熊猫",
        "猫狮",
        "猫头鹰",
        "丁丁猫儿",
        "绿猫鸟",
        "猫鼬",
        "猫鱼",
        "玻璃猫",
        "猫眼",
        "猫蛱蝶",
    ]

    def dog_cat_name_recognizer(name):
        if name in dog_labels:
            return "dog"
        elif name in cat_labels:
            return "cat"
        elif name not in forbidden_words:
            for dog_suffix in dog_suffixs:
                if name.endswith(dog_suffix):
                    return "dog"
            for cat_suffix in cat_suffixs:
                if name.endswith(cat_suffix):
                    return "cat"
        return None

    classifier = getPaddleResnet50AnimalsClassifier()

    def paddleAnimalDetectionResultToList(result):
        resultDict = result[0]
        resultList = [(key, value) for key, value in resultDict.items()]
        resultList.sort(key=lambda item: -item[1])
        return resultList

    def translateResultListToDogCatList(resultList):
        final_result_list = []
        for name, confidence in resultList:
            new_name = dog_cat_name_recognizer(name)
            final_result_list.append((new_name, confidence))
        return final_result_list

    dataList = []
    for frame in getVideoFrameIteratorWithFPS(videoPath, -1, -1, fps=1):
        padded_resized_frame = resizeImageWithPadding(
            frame, 224, 224, border_type="replicate"
        )  # pass the test only if three of these containing 'cats'
        result = classifier.classification(
            images=[padded_resized_frame], top_k=3, use_gpu=False
        )  # check it?
        resultList = paddleAnimalDetectionResultToList(result)
        final_result_list = translateResultListToDogCatList(resultList)
        if debug:
            sprint("RESULT LIST:", final_result_list)
        detections = []
        for index, (label, confidence) in enumerate(final_result_list):
            scope = final_result_list[index:]
            scope_confidences = [elem[1] for elem in scope if elem[0] == label]
            output = multiParameterExponentialNetwork(
                *scope_confidences,
                input_bias=input_bias,
                curve_function_kwargs=curve_function_kwargs,
            )
            # treat each as a separate observation in this frame.
            detections.append({"identity": label, "confidence": output})
        dataList.append({"detections": detections})
        # now we apply the thing? the yolov5 thing?
    detectionConfidence = calculateVideoMeanDetectionConfidence(dataList)
    filter_result = detectionConfidenceFilter(
        detectionConfidence, filter_dict=filter_dict, logic=logic
    )
    # print("DATALIST", dataList)
    # print("DETECTION CONFIDENCE", detectionConfidence)
    # print("FILTER RESULT", filter_result)
    # breakpoint()
    return filter_result


def yolov5_bezier_paddlehub_resnet50_dog_cat_video_filter(
    videoPath,
    debug=False,
    filter_dict={
        "dog": {"min": 0.5},
        "cat": {"min": 0.5},
    },
    logic: Literal["AND", "OR"] = "OR",
    input_bias=0.0830047243746045,
    skew=-0.4986098769473948,
    threshold=0.5,
    dog_label_file_path="/root/Desktop/works/pyjom/tests/animals_paddlehub_classification_resnet/dogs.txt",
    cat_label_file_path="/root/Desktop/works/pyjom/tests/animals_paddlehub_classification_resnet/cats.txt",
):
    if debug:
        sprint("checking video: %s" % videoPath)
    filter_result = yolov5VideoDogCatDetector(
        videoPath, filter_dict=filter_dict, logic=logic, debug=debug
    )  # this is for short video. not for long video. long video needs to be sliced into smaller chunks
    # sprint("FILTER PASSED?", filter_result)
    if not filter_result:
        if debug:
            sprint("CHECKING WITH BEZIER CURVE AND RESNET50")
        filter_result = bezierPaddleHubResnet50VideoDogCatDetector(
            videoPath,
            debug=debug,
            input_bias=input_bias,
            skew=skew,
            threshold=threshold,
            dog_label_file_path=dog_label_file_path,
            cat_label_file_path=cat_label_file_path,
        )
    if not filter_result:
        if debug:
            print("FILTER FAILED")
    else:
        if debug:
            print("FILTER PASSED")
    return filter_result


########################### DOG CAT DETECTION #########################

########################### NSFW FILTER FOR VIDEO #########################


@lru_cache(maxsize=1)
def isNSFWServerUp(port=8511, message="nsfw nodejs server"):
    waitForServerUp(port, message)


def processNSFWServerImageReply(reply):
    mDict = {}
    for elem in reply:
        className, probability = elem["className"], elem["probability"]
        mDict.update({className: probability})
    return mDict


def processNSFWReportArray(
    NSFWReportArray,
    average_classes=["Neutral"],
    get_max_classes=["Drawing", "Porn", "Sexy", "Hentai"],
):
    assert set(average_classes).intersection(set(get_max_classes)) == set()
    NSFWReport = {}
    for element in NSFWReportArray:
        for key in element.keys():
            NSFWReport[key] = NSFWReport.get(key, []) + [element[key]]
    for average_class in average_classes:
        NSFWReport[average_class] = superMean(NSFWReport.get(average_class, [0]))
    for get_max_class in get_max_classes:
        NSFWReport[get_max_class] = superMax(NSFWReport.get(get_max_class, [0]))
    return NSFWReport


from pyjom.commons import checkMinMaxDict

# you can reuse this, really.
def NSFWFilter(
    NSFWReport,
    filter_dict={
        "Neutral": {"min": 0.5},
        "Sexy": {"max": 0.5},
        "Porn": {"max": 0.5},
        "Hentai": {"max": 0.5},
        "Drawing": {"max": 0.5},
    },
    debug=False,
):
    for key in filter_dict:
        value = NSFWReport.get(key, 0)
        key_filter = filter_dict[key]
        result = checkMinMaxDict(value, key_filter)
        if not result:
            if debug:
                print("not passing NSFW filter: %s" % key)
                print("value: %s" % value)
                print("filter: %s" % str(key_filter))
            return False
    return True


from lazero.filesystem import tmpfile
import requests


def NSFWVideoFilter(
    videoPath,
    tmpdirPath="/dev/shm/medialang/nsfw",
    fps=1,
    gateway="http://localhost:8511/",
    debug=False,
    filter_dict={
        "Neutral": {"min": 0.3},
        "Sexy": {"max": 0.65},
        "Porn": {"max": 0.65},
        "Hentai": {"max": 0.65},
        "Drawing": {"max": 0.65},
    },
):
    source = videoPath
    result = False
    with tmpdir(path=tmpdirPath) as T:
        responses = []
        for frame in getVideoFrameIteratorWithFPS(source, -1, -1, fps=fps):
            padded_resized_frame = resizeImageWithPadding(
                frame, 224, 224, border_type="replicate"
            )
            # i'd like to view this.
            basename = "{}.jpg".format(uuid.uuid4())
            jpg_path = os.path.join(tmpdirPath, basename)
            with tmpfile(path=jpg_path) as TF:
                cv2.imwrite(jpg_path, padded_resized_frame)
                files = {"image": (basename, open(jpg_path, "rb"), "image/jpeg")}
                r = requests.post(
                    gateway + "nsfw", files=files
                )  # post gif? or just jpg?
                try:
                    response_json = r.json()
                    response_json = processNSFWServerImageReply(response_json)
                    # breakpoint()
                    # print("RESPONSE:", response_json)
                    responses.append(
                        response_json  # it contain 'messages'
                    )  # there must be at least one response, i suppose?
                except:
                    import traceback

                    traceback.print_exc()
                    print("error when processing NSFW server response")
        NSFWReport = processNSFWReportArray(responses)
        # print(NSFWReport)
        # breakpoint()
        result = NSFWFilter(NSFWReport, filter_dict=filter_dict, debug=debug)
        if result:
            if debug:
                print("NSFW test passed.")
                print("source %s" % source)
    return result


########################### NSFW FILTER FOR VIDEO #########################
