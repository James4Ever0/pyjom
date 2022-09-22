from pyjom.commons import *
import numpy as np
import cv2

from functools import lru_cache


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

@lru_cache(maxsize=1)
def getEasyOCRReader(langs:tuple, gpu=True, recognizer=False):
    import easyocr

    # no metal? no dbnet18?
    reader = easyocr.Reader(langs, gpu=gpu, recognizer=recognizer)
    return reader


@lru_cache(maxsize=30)
def getImageTextAreaRecognized(
    image, langs: tuple = ("en",), gpu=True, recognizer=False, return_res=False
):
    reader = getEasyOCRReader(langs, gpu=gpu, recognizer=recognizer)
    if type(image) == str:
        image = cv2.imread(image)
    frame = image
    height, width = frame.shape[:2]
    res = (width, height)
    detection, recognition = reader.detect(frame)  # not very sure.
    if return_res:
        return res, (detection, recognition)
    else:
        return detection, recognition

def imageFourCornersInpainting(image):
    if type(image) == str:
        image = cv2.imread(image)
    defaultHeight, defaultWidth = image.shape[:2]
    fourCorners = getFourCorners(0,0, defaultWidth, defaultHeight)
    img = np.zeros((defaultHeight, defaultWidth))
    for corner in fourCorners:
    

def getImageTextAreaRatio(
    image,
    langs: tuple = ("en",),
    gpu=True,
    recognizer=False,
    debug=False,
    inpaint=False,
):
    res, (detection, recognition) = getImageTextAreaRecognized(
        image, langs=langs, gpu=gpu, recognizer=recognizer, return_res=True
    )
    width, height = res
    img = np.zeros((height, width))
    if detection == [[]]:
        diagonalRects = []
    else:
        diagonalRects = [LRTBToDiagonal(x) for x in detection[0]]
    for x1, y1, x2, y2 in diagonalRects:
        w, h = x2 - x1, y2 - y1
        x, y = x1, y1
        cv2.rectangle(img, (x, y), (x + w, y + h), 255, -1)
    # calculate the portion of the text area.
    textArea = np.sum(img)
    textAreaRatio = (textArea / 255) / (width * height)
    if debug:
        print("text area: {:.2f} %".format(textAreaRatio))
        cv2.imshow("TEXT AREA", img)
        cv2.waitKey(0)
    if inpaint:
        return cv2.inpaint(image, img, 3, cv2.INPAINT_TELEA)
    return textAreaRatio


def LRTBToDiagonal(lrtb):
    left, right, top, bottom = lrtb
    x0, y0, x1, y1 = left, top, right, bottom
    return (x0, y0, x1, y1)


def imageDenoise(image):
    shape = image.shape
    if len(shape) == 3:
        if shape[2] == 3:
            return cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 21)
    return cv2.fastNlMeansDenoising(image, None, 4, 7, 35)


def getImageColorCentrality(
    image,
    sample_size_limit=5000,
    epsilon=0.01,  # shit man.
    shift=2,
    n_clusters=5,
    batch_size=45,
    max_no_improvement=10,
):
    # image is of numpy.array
    # multiple centers.
    # CENTER: [246.76865924 226.40763256 216.41472476]
    # POSITIVE COUNT: 95497
    # SUM: 286491.0 MIN: 0 MAX: 3
    # NEARBY CENTER PERCENTAGE: 6.74 %
    # CENTRALITY: 7.32 %
    import numpy as np

    # image = cv2.imread(src)
    shape = image.shape
    if len(shape) > 3 or len(shape) < 2:
        print("weird image shape for getImageColorCentrality:", shape)
        breakpoint()
    if len(shape) == 2:
        image = image.reshape(-1, -1, 1)
    # for i in range(3):
    #     image[:,:,i] = i

    # col_0, col_1 = shape[:2]

    # coords = []

    # for c0 in range(col_0):
    #     for c1 in range(col_1):
    #         coords.append((c0,c1))

    # coords = np.array(coords)

    # print(image.reshape(-1,3))
    reshapedImage = image.reshape(-1, 3)  # are you sure about this?
    length, color_channels = reshapedImage.shape

    reshapedImageIndexs = np.arange(0, length)
    # so now it is good.
    sampleIndexs = np.random.choice(
        reshapedImageIndexs, size=min(sample_size_limit, length)
    )
    # print(sampleIndexs)
    # print(sampleIndexs.shape)

    sample = reshapedImageIndexs[sampleIndexs]
    sample = reshapedImage[sample, :]
    # print(sample)
    # print(sample.shape)

    # breakpoint()
    # sampleCoords = coords[sampleIndexs]
    # sample = np.hstack([sample, sampleCoords])
    # print(sample)
    # print(sample.shape)
    # breakpoint()
    # warning: OOM?
    # now cluster shit shall we?
    # from sklearn.neighbors import NearestNeighbors
    # neigh = NearestNeighbors(n_neighbors=5)
    # X = sample
    # neigh.fit(X)
    # A = neigh.kneighbors_graph(X)
    # A.toarray()
    # print(A)
    # print(A.shape) # sparse matrix? wtf?
    # from sklearn.cluster import MiniBatchKMeans  # better?

    from sklearn.cluster import KMeans

    X = sample
    # kmeans = KMeans(n_clusters=5).fit(X) # not deterministic please?
    # here we've got issue.
    # import numpy as np
    # np.seterr(all='ignore')
    kmeans_model = KMeans(init="k-means++", n_clusters=n_clusters)
    kmeans = kmeans_model.fit(X)  # fix this shit
    # keep popping up error logs.
    # kmeans = MiniBatchKMeans(
    #     init="k-means++",
    #     n_clusters=n_clusters,
    #     batch_size=batch_size,
    #     # n_init=10,
    #     max_no_improvement=max_no_improvement,
    #     verbose=0,
    # ).fit(X)
    # from lazero.utils import inspectObject
    # inspectObject(kmeans)
    # breakpoint()
    # labels = kmeans.labels_
    cluster_centers = kmeans.cluster_centers_
    # print(labels)
    # print(cluster_centers)

    # sample_size = len(sampleIndexs) # this is the real sample size.

    # label_percentage = {
    #     x: np.count_nonzero(labels == x) / sample_size for x in range(n_clusters)
    # }

    flagged_image = image.copy()
    flagged_image[:, :, :] = 1  # every element is 1 now.
    percents = []
    for center in cluster_centers:
        # fetch area nearby given center
        # center = center5[:3]
        # center_int = center.astype(np.uint8)
        # i just don't know what the fuck is going on here.
        upper = center + shift
        lower = center - shift
        mask = cv2.inRange(image, lower, upper)
        # not image.
        output = cv2.bitwise_and(flagged_image, flagged_image, mask=mask)
        # print(output)
        # print(output.shape)
        mOutput = output.reshape(-1, 3)
        mOutput = np.sum(mOutput, axis=1)
        # breakpoint()
        positive_count = np.count_nonzero(abs(mOutput - 3) < epsilon)
        percent = positive_count / len(mOutput)
        # print(mOutput)
        # print(mOutput.shape)
        # breakpoint()
        # print("CENTER:",center)
        # print('POSITIVE COUNT:', positive_count)
        # mSum = sum(mOutput)
        # print("SUM:", mSum, "MIN:", min(mOutput), 'MAX:', max(mOutput))
        # print("NEARBY CENTER PERCENTAGE: {:.2f} %".format(percent*100))
        percents.append(percent)
    max_nearby_center_percentage = max(percents)
    print(
        "NEARBY CENTER PERCENTAGE: {:.2f} %".format(max_nearby_center_percentage * 100)
    )
    centrality = sum(percents)
    print("CENTRALITY: {:.2f} %".format(centrality * 100))
    del kmeans
    del kmeans_model
    return centrality, max_nearby_center_percentage


import math


def scanImageWithWindowSizeAutoResize(
    image,
    width,
    height,
    return_direction=False,
    threshold=0.1,  # minimum 'fresh' area left for scanning
):  # shall you use torch? no?
    shape = image.shape
    assert len(shape) == 3
    ih, iw, channels = shape
    targetWidth = max(width, math.floor(iw * height / ih))
    targetHeight = max(height, math.floor(ih * width / iw))
    resized = cv2.resize(
        image, (targetWidth, targetHeight), interpolation=cv2.INTER_CUBIC
    )
    # determine scan direction here.
    imageSeries = []
    if targetWidth / targetHeight == width / height:
        imageSeries = [resized]  # as image series.
        direction = None
    elif targetWidth / targetHeight < width / height:
        direction = "vertical"
        # the scanning is along the vertical axis, which is the height.
        index = 0
        while True:
            start, end = height * index, height * (index + 1)
            if start < targetHeight:
                if end > targetHeight:
                    if 1 - (end - targetHeight) / targetHeight >= threshold:
                        end = targetHeight
                        start = targetHeight - height
                    else:
                        break
                # other conditions, just fine
            else:
                break  # must exit since nothing to scan.
            cropped = resized[start:end, :, :]  # height, width, channels
            imageSeries.append(cropped)
            index += 1
    else:
        direction = "horizontal"
        index = 0
        while True:
            start, end = width * index, width * (index + 1)
            if start < targetWidth:
                if end > targetWidth:
                    if 1 - (end - targetWidth) / targetWidth >= threshold:
                        end = targetWidth
                        start = targetWidth - width
                    else:
                        break
                # other conditions, just fine
            else:
                break  # must exit since nothing to scan.
            cropped = resized[:, start:end, :]  # height, width, channels
            imageSeries.append(cropped)
            index += 1
    if return_direction:
        return imageSeries, direction
    else:
        return imageSeries


from typing import Literal


def resizeImageWithPadding(
    image,
    width,
    height,
    border_type: Literal["constant_black", "replicate"] = "constant_black",
):
    shape = image.shape
    assert len(shape) == 3
    ih, iw, channels = shape
    targetWidth = min(width, math.floor(iw * height / ih))
    targetHeight = min(height, math.floor(ih * width / iw))
    resized = cv2.resize(
        image, (targetWidth, targetHeight), interpolation=cv2.INTER_CUBIC
    )
    BLACK = [0] * channels
    top = max(0, math.floor((height - targetHeight) / 2))
    bottom = max(0, height - targetHeight - top)
    left = max(0, math.floor((width - targetWidth) / 2))
    right = max(0, width - targetWidth - left)
    if border_type == "constant_black":
        padded = cv2.copyMakeBorder(
            resized, top, bottom, left, right, cv2.BORDER_CONSTANT, value=BLACK
        )
    elif border_type == "replicate":
        padded = cv2.copyMakeBorder(
            resized, top, bottom, left, right, cv2.BORDER_REPLICATE, value=BLACK
        )
    else:
        raise Exception("unknown border_type: %s" % border_type)
    return padded
