# funny sight.
# we plan to put automatic watermark detection here. no issue?
# import numpy as np
from pyjom.commons import *
from pyjom.mathlib import *
import cv2
# import cv2


def checkXYWH(XYWH,canvas,minArea = 20):
    x,y,w,h = XYWH
    width, height = canvas
    if x >= width-1 or y >= height-1:
        return False, None
    if x == 0:
        x = 1
    if y == 0:
        y = 1
    if x+w >= width:
        w = width-x-1
        if w <= 2:
            return False, None
    if y+h >= height:
        h = height-y-1
        if h <= 2:
            return False, None
    if w*h <= minArea:
        return False, None
    return True, (x,y,w,h)


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
    # if not iterate:
    # print("NOT ITERATING")
    def nonIterator(cap,samplePopulation):
        imageList = []
        for sampleIndex in progressbar.progressbar(samplePopulation):
            cap.set(cv2.CAP_PROP_POS_FRAMES, sampleIndex)
            success, image = cap.read()
            if success:
                # print("APPENDING!")
                imageList.append(image.copy())
        return imageList
    def iterator(cap,samplePopulation):
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

def detectStationaryLogoOverTime(filepath,start,end,sample_size=60):
    imageSet = getVideoFrameSampler(filepath, start, end, sample_size=sample_size)
    # what is this src?
    # from src import *

    ###########
    import sys, os
    import cv2
    import numpy as np
    import warnings
    from matplotlib import pyplot as plt
    import math
    import numpy
    import scipy, scipy.fftpack

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
        gradx = list(map(lambda x: cv2.Sobel(x, cv2.CV_64F, 1, 0, ksize=KERNEL_SIZE), images)) # this is py3 my friend?
        grady = list(map(lambda x: cv2.Sobel(x, cv2.CV_64F, 0, 1, ksize=KERNEL_SIZE), images)) # this is py3 my friend?

        # Compute median of grads
        print("Computing median gradients.")
        # print(gradx,grady)
        # breakpoint()
        Wm_x = np.median(np.array(gradx), axis=0)
        Wm_y = np.median(np.array(grady), axis=0)
        # slow as hell?

        return (Wm_x, Wm_y, gradx, grady)

    def poisson_reconstruct(gradx, grady, kernel_size=KERNEL_SIZE, num_iters=100, h=0.1, 
            boundary_image=None, boundary_zero=True):
        """
        Iterative algorithm for Poisson reconstruction. 
        Given the gradx and grady values, find laplacian, and solve for image
        Also return the squared difference of every step.
        h = convergence rate
        """
        fxx = cv2.Sobel(gradx, cv2.CV_64F, 1, 0, ksize=kernel_size)
        fyy = cv2.Sobel(grady, cv2.CV_64F, 0, 1, ksize=kernel_size)
        laplacian = fxx + fyy
        m,n,p = laplacian.shape # three channels?

        if boundary_zero == True:
            est = np.zeros(laplacian.shape)
        else:
            assert(boundary_image is not None)
            assert(boundary_image.shape == laplacian.shape)
            est = boundary_image.copy()

        est[1:-1, 1:-1, :] = np.random.random((m-2, n-2, p))
        loss = []

        for i in range(num_iters):
            old_est = est.copy()
            est[1:-1, 1:-1, :] = 0.25*(est[0:-2, 1:-1, :] + est[1:-1, 0:-2, :] + est[2:, 1:-1, :] + est[1:-1, 2:, :] - h*h*laplacian[1:-1, 1:-1, :])
            error = np.sum(np.square(est-old_est))
            loss.append(error)

        return (est)
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
    mFinalDelogoFilters = []
    for cnt in cnts2:
        x, y, w, h = cv2.boundingRect(cnt)  # Draw the bounding box image=
        delogoCommand = "delogo_{}_{}_{}_{}".format(x,y,w,h)
        # print(delogoCommand)
        # print('width:{} height:{}'.format(b,a))
        # if b< x+w or a<y+h:
        #     print("ERROR!")
        #     breakpoint()
        mFinalDelogoFilters.append(delogoCommand)
        # cv2.rectangle(output, (x,y), (x+w,y+h), (0,0,255),2)
        # cv2.rectangle(myMask2, (x, y), (x + w, y + h), 255, -1)
    print("TOTAL {} STATIONARY LOGOS.".format(len(cnts2)))
    # breakpoint()
    # get the final dictionary
    if len(mFinalDelogoFilters) == 0:
        return {}
    else:
        delogoCommandSet= "|".join(mFinalDelogoFilters)
        # print(delogoCommandSet)
        # breakpoint()
        return {delogoCommandSet: [(start, end)]}
    
def detectPipRegionOverTime(videoPath, start, end, method = "skim", algo='frame_difference'): # shall be some parameters here.
    # if it is 'skim' we will sample it every 20 frames.
    import pybgs as bgs
    assert algo in ['frame_difference', 'weighted_moving_average']
    if algo == 'frame_difference':
        algorithm = bgs.FrameDifference()
        # much faster.
    else:
        algorithm = bgs.WeightedMovingAverage()
        # slower. don't know if it works or not.
        # it does produce different results.
    # otherwise we do it frame by frame.
    assert method in ['skim','framewise']
    pipFrames = []
    if method == 'framewise':
        iterator = getVideoFrameIterator(videoPath,start,end)
    else:
        sample_rate = max(1,estimated_sample_rate )
        iterator = getVideoFrameIterator(videoPath, start, end, sample_rate=sample_rate)
        for frame in iterator:
            img_output = algorithm.apply(frame)
            pipFrames.append([(min_x, min_y), (max_x, max_y)].copy())