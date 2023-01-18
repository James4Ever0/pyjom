from pyjom.commons import *
import numpy as np
import cv2

from functools import lru_cache
from lazero.utils.tools import flattenUnhashableList
from typing import Literal


def imageCropWithDiagonalRectangle(
    image, diagonalRectangle, order: Literal["opencv", "normal"] = "opencv"
):
    # order is opencv.
    assert order in ["opencv", "normal"]
    x0, y0, x1, y1 = flattenUnhashableList(diagonalRectangle)
    imageShape = image.shape
    if len(imageShape) == 3:
        if order == "opencv":
            return image[y0:y1, x0:x1, :]
        elif order == "normal":
            return image[x0:x1, y0:y1, :]
    elif len(imageShape) == 2:
        if order == "opencv":
            return image[y0:y1, x0:x1]
        elif order == "normal":
            return image[x0:x1, y0:y1]
    else:
        raise Exception("unknown image shape:", imageShape)


def draw_bounding_box_with_contour(
    contours, image, area_threshold=20, debug=False
):  # are you sure?
    # this is the top-k approach.
    # Call our function to get the list of contour areas
    # cnt_area = contour_area(contours)

    # Loop through each contour of our image
    x0, y0, x1, y1 = [None] * 4
    for i in range(0, len(contours), 1):
        cnt = contours[i]
        # Only draw the the largest number of boxes
        if cv2.contourArea(cnt) > area_threshold:
            # if (cv2.contourArea(cnt) > cnt_area[number_of_boxes]):

            # Use OpenCV boundingRect function to get the details of the contour
            x, y, w, h = cv2.boundingRect(cnt)
            if x0 == None:
                x0, y0, x1, y1 = x, y, x + w, y + h
            if x < x0:
                x0 = x
            if y < y0:
                y0 = y
            if x + w > x1:
                x1 = x + w
            if y + h > y1:
                y1 = y + h
            # Draw the bounding box

    if x0 is not None:
        if debug:
            image = cv2.rectangle(image, (x0, y0), (x1, y1), (0, 0, 255), 2)
            cv2.imshow("with_bounding_box", image)
            cv2.waitKey(0)

    if x0 is None:
        height, width = image.shape[:2]
        x0, y0, x1, y1 = 0, 0, width, height
    return (x0, y0), (x1, y1)


def imageLoader(image):
    if type(image) == str:
        if os.path.exists(image):
            image = cv2.imread(image)
        elif image.startswith("http"):
            import requests

            r = requests.get(image)
            content = r.content
            content = np.asarray(bytearray(content), dtype="uint8")
            image = cv2.imdecode(content, cv2.IMREAD_COLOR)
        else:
            raise Exception("unknown image link: %s" % image)
    return image


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
    fourCorners = [[(a + x, b + y), (c + x, d + y)] for [(a, b), (c, d)] in fourCorners]
    return fourCorners


@lru_cache(maxsize=1)
def getEasyOCRReader(langs: tuple, gpu=True, recognizer=False):
    import easyocr

    # no metal? no dbnet18?
    reader = easyocr.Reader(langs, gpu=gpu, recognizer=recognizer)
    return reader


# @lru_cache(maxsize=30)
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


from typing import Literal


def partial_blur(image0, mask, kernel=None):
    # need improvement. malnly the boundary.
    if kernel is None:
        height, width = image0.shape[:2]
        kernel_w = max(int(width / 40), 1) * 4
        kernel_h = max(int(height / 40), 1) * 4
    else:
        kernel_w, kernel_h = kernel
        kernel_w = max(int(kernel_w / 4), 1) * 4
        kernel_h = max(int(kernel_h / 4), 1) * 4
    kernel = (kernel_w, kernel_h)

    mask_total = mask
    inv_mask_total = 255 - mask_total
    # mask0 = mask
    # mask0 = mask/255
    # inv_mask0 = inv_mask/255
    non_blur_image = cv2.bitwise_and(image0, image0, mask=inv_mask_total)
    blur_image0 = cv2.blur(image0, kernel)  # half quicklier.
    blur_image0 = cv2.bitwise_and(blur_image0, blur_image0, mask=mask_total)
    dst0 = blur_image0 + non_blur_image
    return dst0


def imageInpainting(image, mask, method: Literal["inpaint", "blur"] = "inpaint"):
    if method == "inpaint":
        return cv2.inpaint(image, mask, 3, cv2.INPAINT_TELEA)
    elif method == "blur":
        return partial_blur(image, mask)
    else:
        raise Exception("image inpainting method not supported:", method)


def imageFourCornersInpainting(image, method="inpaint"):
    if type(image) == str:
        image = cv2.imread(image)
    defaultHeight, defaultWidth = image.shape[:2]
    fourCorners = getFourCorners(0, 0, defaultWidth, defaultHeight)
    img = np.zeros((defaultHeight, defaultWidth), dtype=np.uint8)
    for (x1, y1), (x2, y2) in fourCorners:
        w, h = x2 - x1, y2 - y1
        x, y = x1, y1
        cv2.rectangle(img, (x, y), (x + w, y + h), 255, -1)
    return imageInpainting(image, img, method=method)


def getImageTextAreaRatio(
    image,
    langs: tuple = ("en",),
    gpu=True,
    recognizer=False,
    debug=False,
    inpaint=False,
    method="inpaint",
    edgeDetection=False,
):
    image_passed = image.copy()
    if edgeDetection:
        image_passed = cv2.Canny(image_passed, 20, 210, apertureSize=3)
    res, (detection, recognition) = getImageTextAreaRecognized(
        image_passed, langs=langs, gpu=gpu, recognizer=recognizer, return_res=True
    )
    width, height = res
    img = np.zeros((height, width), dtype=np.uint8)
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
        return imageInpainting(image, img, method=method)
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
    width: Union[int, None],
    height: Union[int, None],
    border_type: Literal["constant_black", "replicate"] = "constant_black",
):
    assert any([type(param) == int for param in [width, height]])
    shape = image.shape
    assert len(shape) == 3
    ih, iw, channels = shape
    if width is None:
        width = max(1, math.floor((height / ih) * iw))
    if height is None:
        height = max(1, math.floor((width / iw) * ih))

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

BEZIER_PADDLE_RESNET50_IMAGE_DOG_CAT_DETECTOR_SERVER_ENDPOINT = "analyzeImage"
BEZIER_PADDLE_RESNET50_IMAGE_DOG_CAT_DETECTOR_SERVER_PORT = 4675
BEZIER_PADDLE_RESNET50_IMAGE_DOG_CAT_DETECTOR_SERVER_HELLO = (
    "Bezier PaddleHub Resnet50 Image DogCat Detector Server"
)

from pyjom.config.shared import pyjom_config

# TODO: support serving and with redis lock
from lazero.network.checker import waitForServerUp


def bezierPaddleHubResnet50ImageDogCatDetectorServerChecker(
    port=BEZIER_PADDLE_RESNET50_IMAGE_DOG_CAT_DETECTOR_SERVER_PORT,
    message=BEZIER_PADDLE_RESNET50_IMAGE_DOG_CAT_DETECTOR_SERVER_HELLO,
):
    waitForServerUp(port=port, message=message)


# fuck?
if not pyjom_config["BEZIER_PADDLE_RESNET50_IMAGE_DOG_CAT_DETECTOR_SERVER_INSTANCE"]:
    bezierPaddleHubResnet50ImageDogCatDetectorServerChecker()


def bezierPaddleHubResnet50ImageDogCatDetectorClient(
    image,
    port=BEZIER_PADDLE_RESNET50_IMAGE_DOG_CAT_DETECTOR_SERVER_PORT,
    endpoint=BEZIER_PADDLE_RESNET50_IMAGE_DOG_CAT_DETECTOR_SERVER_ENDPOINT,
    input_bias=0.0830047243746045,
    skew=-0.4986098769473948,
    # threshold=0.5,
    dog_label_file_path="/root/Desktop/works/pyjom/tests/animals_paddlehub_classification_resnet/dogs.txt",
    cat_label_file_path="/root/Desktop/works/pyjom/tests/animals_paddlehub_classification_resnet/cats.txt",
    debug=False,
):
    isString = type(image) == str
    import requests

    url = "http://localhost:{}/{}".format(port, endpoint)
    import numpy_serializer

    if type(image) == np.ndarray:
        image = numpy_serializer.to_bytes(image)
    data = dict(image=image)
    params = dict(
        input_bias=input_bias,
        isBytes=not isString,
        skew=skew,
        dog_label_file_path=dog_label_file_path,
        cat_label_file_path=cat_label_file_path,
        debug=debug,
    )
    r = requests.post(url, data=data, params=params)
    # what is the result? fuck?
    return r.json()


def bezierPaddleHubResnet50ImageDogCatDetectorCore(
    image,
    input_bias=0.0830047243746045,
    skew=-0.4986098769473948,
    # threshold=0.5,
    dog_label_file_path="/root/Desktop/works/pyjom/tests/animals_paddlehub_classification_resnet/dogs.txt",
    cat_label_file_path="/root/Desktop/works/pyjom/tests/animals_paddlehub_classification_resnet/cats.txt",
    debug=False,
    use_gpu=False,
    dog_suffixs=["狗", "犬", "梗"],
    cat_suffixs=["猫"],
    forbidden_words=[
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
    ],
):

    curve_function_kwargs = {
        "start": (0, 0),
        "end": (1, 1),
        "skew": skew,
    }  # maximize the output.
    if type(image) == str:
        image = cv2.imread(image)
    frame = image
    # ends with this, and not containing forbidden words.
    dog_labels = labelFileReader(dog_label_file_path)
    cat_labels = labelFileReader(cat_label_file_path)

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

    # dataList = []
    # for frame in getVideoFrameIteratorWithFPS(videoPath, -1, -1, fps=1):
    padded_resized_frame = resizeImageWithPadding(
        frame, 224, 224, border_type="replicate"
    )  # pass the test only if three of these containing 'cats'
    result = classifier.classification(
        images=[padded_resized_frame], top_k=3, use_gpu=use_gpu  # cuda oom?
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
    return detections


def bezierPaddleHubResnet50ImageDogCatDetector(
    image,
    input_bias=0.0830047243746045,
    skew=-0.4986098769473948,
    # threshold=0.5,
    dog_label_file_path="/root/Desktop/works/pyjom/tests/animals_paddlehub_classification_resnet/dogs.txt",
    cat_label_file_path="/root/Desktop/works/pyjom/tests/animals_paddlehub_classification_resnet/cats.txt",
    debug=False,
    use_gpu=False,
    as_client=True,  # by default!
):
    if as_client:
        return bezierPaddleHubResnet50ImageDogCatDetectorClient(
            image,
            input_bias=input_bias,
            skew=skew,
            dog_label_file_path=dog_label_file_path,
            cat_label_file_path=cat_label_file_path,
            debug=debug,
        )
    # from pyjom.imagetoolbox import resizeImageWithPadding
    detections = bezierPaddleHubResnet50ImageDogCatDetectorCore(
        image,
        input_bias=input_bias,
        skew=skew,
        dog_label_file_path=dog_label_file_path,
        cat_label_file_path=cat_label_file_path,
        debug=debug,
        use_gpu=use_gpu,
    )
    return detections


# TODO: create/get a redis based lock when doing image checks.
import redis_lock
import redis
from pyjom.commons import commonRedisPort

redis_connection = redis.StrictRedis(port=commonRedisPort)


def bezierPaddleHubResnet50ImageDogCatDetectorServer(
    server_port=BEZIER_PADDLE_RESNET50_IMAGE_DOG_CAT_DETECTOR_SERVER_PORT,
    endpoint=BEZIER_PADDLE_RESNET50_IMAGE_DOG_CAT_DETECTOR_SERVER_ENDPOINT,
    serverHelloMessage: str = BEZIER_PADDLE_RESNET50_IMAGE_DOG_CAT_DETECTOR_SERVER_HELLO,
    connection: redis.Redis = redis_connection,
    lockName: str = "bezier_paddlehub_resnet50_image_dog_cat_detector_server",
    timeout: float = 10,
    expire: float = 60,
):

    from fastapi import FastAPI, Body
    import numpy_serializer

    app = FastAPI()

    @app.get("/")
    def serverHello():
        return serverHelloMessage

    @app.post("/" + endpoint)
    def receiveImage(
        image: bytes = Body(default=None),
        isBytes: bool = False,
        encoding: str = "utf-8",
        debug: bool = False,
        input_bias: float = 0.0830047243746045,
        skew: float = -0.4986098769473948,
        dog_label_file_path: str = "/root/Desktop/works/pyjom/tests/animals_paddlehub_classification_resnet/dogs.txt",
        cat_label_file_path: str = "/root/Desktop/works/pyjom/tests/animals_paddlehub_classification_resnet/cats.txt",
        download_timeout: int = 2,
    ):
        detections = []  # nothing good.

        try:
            lock = redis_lock.Lock(connection, name=lockName, expire=expire)
            if lock.acquire(blocking=True, timeout=timeout):
                # return book
                # print('image type:',type(image))
                # print(image)
                import urllib.parse

                image = image.removeprefix(b"image=")  # fuck man.
                image = urllib.parse.unquote_to_bytes(image)
                if debug:
                    print("isBytes:", isBytes)
                if not isBytes:
                    image = image.decode(encoding)  # fuck?
                    # read image from path, url
                    if image.startswith("http"):
                        import requests

                        img_bytes = requests.get(
                            image, proxies=None, timeout=download_timeout
                        ).content
                        # warning! you deal with gif somehow!
                        import tempfile

                        with tempfile.NamedTemporaryFile("wb", suffix=".media") as f:
                            filepath = f.name
                            f.write(img_bytes)
                            try:
                                image = cv2.imread(filepath)
                                if image is None:
                                    cap = cv2.VideoCapture(filepath)
                                    success, image = cap.read()
                                    if not success:
                                        image = None
                            except:
                                import traceback

                                traceback.print_exc()
                                print("error while reading visual media file from web.")
                                print("source url:", image)
                        # nparr = np.fromstring(img_bytes, np.uint8)
                        # image = cv2.imdecode(nparr, flags=1)
                    elif os.path.exists(image):
                        image = cv2.imread(image)
                    else:
                        raise Exception(
                            "image cannot be found as url or filepath:", image
                        )
                else:
                    image = numpy_serializer.from_bytes(image)
                if debug:
                    print("shape?", image.shape)
                    print("image?", image)
                detections = bezierPaddleHubResnet50ImageDogCatDetectorCore(
                    image,
                    input_bias=input_bias,
                    skew=skew,
                    # threshold=0.5,
                    dog_label_file_path=dog_label_file_path,
                    cat_label_file_path=cat_label_file_path,
                    debug=debug,
                )
                lock.release()
                # return detections
        except:
            import traceback

            traceback.print_exc()
        if debug:
            print("DETECTIONS?")
            print(detections)
        return detections

    import uvicorn

    # checking: https://9to5answer.com/python-how-to-use-fastapi-and-uvicorn-run-without-blocking-the-thread

    def run(host="0.0.0.0", port=server_port):
        """
        This function to run configured uvicorn server.
        """
        uvicorn.run(app=app, host=host, port=port)

    run()


def imageCropoutBlackArea(image, cropped_area_threshold=0.1, debug=False, crop=True):
    image = imageLoader(image)
    height, width = image.shape[:2]
    total_area = height * width
    import ffmpeg

    # it must be a existing image.
    from lazero.filesystem.temp import tmpfile
    import uuid

    path = "/dev/shm/cropdetect_ffmpeg_black_border/{}.png".format(str(uuid.uuid4()))
    x, y, x1, y1 = 0, 0, width, height

    with tmpfile(path=path) as TF:
        mediaPath = path
        cv2.imwrite(mediaPath, image)
        stdout, stderr = (
            ffmpeg.input(mediaPath, loop=1, t=1)
            .filter("cropdetect")
            .output("null", f="null")
            .run(capture_stdout=True, capture_stderr=True)
        )

        stdout_decoded = stdout.decode("utf-8")
        stderr_decoded = stderr.decode("utf-8")

        # nothing here.
        # for line in stdout_decoded.split("\n"):
        #     print(line)

        # breakpoint()
        import parse

        common_crops = []

        for line in stderr_decoded.split("\n"):
            line = line.replace("\n", "").strip()
            formatString = "[{}] x1:{x1:d} x2:{x2:d} y1:{y1:d} y2:{y2:d} w:{w:d} h:{h:d} x:{x:d} y:{y:d} pts:{pts:g} t:{t:g} crop={}:{}:{}:{}"
            # print(line)
            result = parse.parse(formatString, line)
            if result is not None:
                # print(result)
                cropString = "{}_{}_{}_{}".format(
                    *[result[key] for key in ["w", "h", "x", "y"]]
                )
                # print(cropString)
                # breakpoint()
                common_crops.append(cropString)
            # [Parsed_cropdetect_0 @ 0x56246a16cbc0] x1:360 x2:823 y1:0 y2:657 w:464 h:656 x:360 y:2 pts:3 t:0.120000 crop=464:656:360:2
            # this crop usually will never change. but let's count?
        area = 0
        # x,x1,y,y1= 0,width, 0, height
        if len(common_crops) > 0:
            common_crops_count_tuple_list = [
                (cropString, common_crops.count(cropString))
                for cropString in set(common_crops)
            ]
            common_crops_count_tuple_list.sort(key=lambda x: -x[1])
            selected_crop_string = common_crops_count_tuple_list[0][0]

            result = parse.parse("{w:d}_{h:d}_{x:d}_{y:d}", selected_crop_string)
            w, h, x, y = [result[key] for key in ["w", "h", "x", "y"]]
            x1, y1 = min(x + w, width), min(y + h, height)
            if x < x1 and y < y1:
                # allow to calculate the area.
                area = (x1 - x) * (y1 - y)
        cropped_area_ratio = 1 - (area / total_area)  # 0.5652352766414517
        # use 0.1 as threshold?
        print("CROPPED AREA RATIO:", cropped_area_ratio)

        if cropped_area_ratio > cropped_area_threshold:
            print("we need to crop this. no further processing needed")
            if debug:
                image_black_cropped = image[y:y1, x:x1]
                cv2.imshow("CROPPED IMAGE", image_black_cropped)
                cv2.waitKey(0)
        else:
            print("image no need to crop black borders. further processing needed")
    diagonalRect = [(x, y), (x1, y1)]
    if crop:
        return imageCropWithDiagonalRectangle(image, diagonalRect)
    return diagonalRect


def imageCropoutBlurArea(
    image, thresh=10, max_thresh=120, min_thresh=50, debug=False, crop=True, value=False
):
    import numpy

    import BlurDetection

    img = imageLoader(image)

    # import sys

    # sys.path.append("/root/Desktop/works/pyjom/")
    # from pyjom.imagetoolbox import imageFourCornersInpainting, getImageTextAreaRatio

    # img = imageFourCornersInpainting(img)
    # img = getImageTextAreaRatio(img, inpaint=True, edgeDetection=True)

    img_fft, val, blurry = BlurDetection.blur_detector(img, thresh=thresh)
    if debug:
        print("this image {0} blurry".format(["isn't", "is"][blurry]))
    msk, result, blurry = BlurDetection.blur_mask(
        img, min_thresh=min_thresh, max_thresh=max_thresh
    )
    if value:
        return result

    inv_msk = 255 - msk

    def display(title, img, max_size=200000):
        assert isinstance(img, numpy.ndarray), "img must be a numpy array"
        assert isinstance(title, str), "title must be a string"
        scale = numpy.sqrt(min(1.0, float(max_size) / (img.shape[0] * img.shape[1])))
        print("image is being scaled by a factor of {0}".format(scale))
        shape = (int(scale * img.shape[1]), int(scale * img.shape[0]))
        img = cv2.resize(img, shape)
        cv2.imshow(title, img)

    # BlurDetection.scripts.display('img', img)
    if debug:
        display("img", img)
        # display("msk", msk)
        display("inv_msk", inv_msk)
    # BlurDetection.scripts.display('msk', msk)
    contours, hierarchy = cv2.findContours(inv_msk, 1, 2)
    rectangle_boundingbox = draw_bounding_box_with_contour(contours, img, debug=debug)
    if crop:
        return imageCropWithDiagonalRectangle(img, rectangle_boundingbox)
    return rectangle_boundingbox


def imageHistogramMatch(image, reference, delta=0.2):
    from color_transfer import color_transfer

    target = imageLoader(image)
    source = imageLoader(reference)
    transfer = color_transfer(source, target)

    import numpy as np

    transfer_02 = (target * (1 - delta) + transfer * delta).astype(np.uint8)
    return transfer_02


def imageDogCatDetectionForCoverExtraction(
    image,
    dog_or_cat: Literal["dog", "cat"] = "dog",
    area_threshold=0.08,  # min area?
    confidence_threshold=0.85,  # this is image quality maybe.
    y_expansion_rate=0.03,  # to make the starting point on y axis less "headless"
    defaultCropWidth=1920,
    defaultCropHeight=1080,
    debug=False,
    debug_show=False,
    crop=False,
    mod=0.8,
):
    # return detected most significant dog area?
    model = configYolov5()

    # dog_or_cat = "dog"

    # Images
    # img = '/media/root/help/pyjom/samples/image/miku_on_green.png'  # or file, Path, PIL, OpenCV, numpy, list
    # img = "/root/Desktop/works/pyjom/samples/image/dog_with_text.jpg"
    # imgPath = "/root/Desktop/works/pyjom/samples/image/dog_blue_sky.png"
    imgPath = image

    # img = cv2.imread(imgPath)
    img = imageLoader(imgPath)

    defaultHeight, defaultWidth = img.shape[:2]
    total_area = defaultHeight * defaultWidth

    # Inference
    results = model(img)

    # print(results)
    # # Results
    # breakpoint()
    animal_detection_dataframe = results.pandas().xyxy[0]
    # results.show()
    # # results.print() # or .show(),

    area = (animal_detection_dataframe["xmax"] - animal_detection_dataframe["xmin"]) * (
        animal_detection_dataframe["ymax"] - animal_detection_dataframe["ymin"]
    )

    animal_detection_dataframe["area_ratio"] = area / total_area

    df = animal_detection_dataframe
    if debug:
        print("DETECTION DATAFRAME")
        print(df)

    new_df = df.loc[
        (df["area_ratio"] >= area_threshold)
        & (df["confidence"] >= confidence_threshold)
        & (df["name"] == dog_or_cat)
    ].sort_values(
        by=["confidence"]
    )  # this one is for 0.13

    # count = new_df.count(axis=0)
    count = len(new_df)
    # print("COUNT: %d" % count)

    # this is just to maintain the ratio.

    # you shall find the code elsewhere?

    allowedHeight = min(
        int(defaultWidth / defaultCropWidth * defaultHeight), defaultHeight
    )
    croppedImageCoverResized = None
    flag = count >= 1
    # if not crop:
    #     return flag
    if flag:
        selected_col = new_df.iloc[0]  # it is a dict-like object.
        # print(new_df)
        if debug:
            print("selected_col")
            print(selected_col)
        # breakpoint()
        # selected_col_dict = dict(selected_col)
        # these are floating point shits.
        # {'xmin': 1149.520263671875, 'ymin': 331.6445007324219, 'xmax': 1752.586181640625, 'ymax': 1082.3826904296875, 'confidence': 0.9185908436775208, 'class': 16, 'name': 'dog', 'area_ratio': 0.13691652620239364}
        x0, y0, x1, y1 = [
            int(selected_col[key]) for key in ["xmin", "ymin", "xmax", "ymax"]
        ]

        y0_altered = max(int(y0 - (y1 - y0) * y_expansion_rate), 0)
        height_current = min((y1 - y0_altered), allowedHeight)  # reasonable?
        width_current = min(
            int((height_current / defaultCropHeight) * defaultCropWidth), defaultWidth
        )  # just for safety. not for mathematical accuracy.
        # height_current = min(allowedHeight, int((width_current/defaultCropWidth)*defaultCropHeight))
        # (x1+x0)/2-width_current/2
        import random

        randStart, randEnd = max((x1 - width_current), 0), min(
            x0, defaultWidth - width_current
        )
        randRange = randEnd - randStart
        randModRange = int(randRange * (1 - mod) / 2)
        randModStart = min(randStart + randModRange, randEnd)
        randModEnd = max(randModStart, randEnd - randModRange)
        x0_framework = random.randint(randModStart, randModEnd)
        framework_XYWH = (x0_framework, y0_altered, width_current, height_current)
        x_f, y_f, w_f, h_f = framework_XYWH
        diagonalRect = [(x_f, y_f), (x_f + w_f, y_f + h_f)]
        if not crop:
            return diagonalRect
        # croppedImageCover = img[y_f : y_f + h_f, x_f : x_f + w_f, :]
        croppedImageCover = imageCropWithDiagonalRectangle(img, diagonalRect)
        # breakpoint()
        # resize image
        croppedImageCoverResized = cv2.resize(
            croppedImageCover, (defaultCropWidth, defaultCropHeight)
        )
        if debug_show:
            cv2.imshow("CROPPED IMAGE COVER", croppedImageCover)
            cv2.imshow("CROPPED IMAGE COVER RESIZED", croppedImageCoverResized)
            # print(selected_col_dict)
            # print(count)
            # breakpoint()
            cv2.waitKey(0)
    else:
        if debug:
            print("NO COVER FOUND.")
    # if not crop:
    # return [(0, 0), (defaultWidth, defaultHeight)]
    return croppedImageCoverResized


def getImageBestConfidenceWithBezierDogCatDetector(
    frame, dog_or_cat: Literal["dog", "cat"] = "dog", debug=False
):
    best_confidence = 0
    detections = bezierPaddleHubResnet50ImageDogCatDetector(
        frame, use_gpu=False
    )  # no gpu avaliable
    mDetections = [x for x in detections if x["identity"] == dog_or_cat]
    mDetections.sort(key=lambda x: -x["confidence"])  # select the best one.
    if len(mDetections) > 0:
        best_confidence = mDetections[0]["confidence"]
        if debug:
            print("BEST CONFIDENCE:", best_confidence)
    return best_confidence


def filterImageBestConfidenceWithBezierDogCatDetector(
    frame,
    dog_or_cat: Literal["dog", "cat"] = "dog",
    debug=False,
    confidence_threshold={"min": 0.7},
):
    best_confidence = getImageBestConfidenceWithBezierDogCatDetector(
        frame, dog_or_cat=dog_or_cat, debug=debug
    )
    return checkMinMaxDict(best_confidence, confidence_threshold)


def imageDogCatCoverCropAdvanced(
    frame,
    dog_or_cat="dog",
    confidence_threshold={"min": 0.7},
    yolov5_confidence_threshold=0.4,
    text_area_threshold={"max": 0.2},
    gpu=True,
    corner=True,
    area_threshold=0.2,
    debug=False,
):
    processed_frame = None
    frame = imageLoader(frame)
    height, width = frame.shape[:2]
    area = height * width

    # detections = bezierPaddleHubResnet50ImageDogCatDetector(
    #     frame, use_gpu=False
    # )  # no gpu avaliable
    # mDetections = [x for x in detections if x["identity"] == dog_or_cat]
    # mDetections.sort(key=lambda x: -x["confidence"])  # select the best one.
    # if len(mDetections) > 0:
    # best_confidence =

    # if best_confidence >0: # just stub.
    #     best_confidence = mDetections[0]["confidence"]
    #     print("BEST CONFIDENCE:", best_confidence)
    # if checkMinMaxDict(best_confidence, confidence_threshold):
    if filterImageBestConfidenceWithBezierDogCatDetector(
        frame,
        dog_or_cat=dog_or_cat,
        debug=debug,
        confidence_threshold=confidence_threshold,
    ):
        # target = getImageTextAreaRatio(frame, inpaint=True, gpu=gpu)
        # target = imageFourCornersInpainting(target)
        # processed_frame = target
        # break
        text_area_ratio = getImageTextAreaRatio(
            frame,
            gpu=gpu,
        )
        # text_area_ratio = getImageTextAreaRatio(frame, gpu=gpu)
        print("TEXT AREA RATIO", text_area_ratio)
        # if animalCropDiagonalRect is not None:
        if checkMinMaxDict(text_area_ratio, text_area_threshold):
            mFrame = getImageTextAreaRatio(frame, gpu=gpu, inpaint=True)
            if corner:
                mFrame = imageFourCornersInpainting(mFrame)
            mFrame = imageCropoutBlackArea(mFrame)
            mFrame = imageCropoutBlurArea(mFrame)
            # cv2.imshow("PRE_FINAL_IMAGE", mFrame)
            # cv2.waitKey(0)
            processed_frame = imageDogCatDetectionForCoverExtraction(
                mFrame,
                dog_or_cat=dog_or_cat,
                confidence_threshold=yolov5_confidence_threshold,
                # area_threshold=0.15,
                crop=True,
                debug=True,
            )
    if processed_frame is not None:
        p_height, p_width = processed_frame.shape[:2]
        p_area = p_height * p_width

        if p_area / area < area_threshold:
            processed_frame = None
        elif not filterImageBestConfidenceWithBezierDogCatDetector(
            frame,
            dog_or_cat=dog_or_cat,
            debug=debug,
            confidence_threshold=confidence_threshold,
        ):
            processed_frame = None

    return processed_frame
