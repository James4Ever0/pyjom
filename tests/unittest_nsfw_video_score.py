# we take max for the concerned ones, and take mean for the unconcerned ones.

from test_commons import *
import requests
from lazero.network.checker import waitForServerUp
from pyjom.videotoolbox import getVideoFrameIteratorWithFPS

gateway = "http://localhost:8511/"

from lazero.utils.importers import cv2_custom_build_init

cv2_custom_build_init()
import cv2

# suggest you not to use this shit.
import math


def scanImageWithWindowSizeAutoResize(
    image, width, height, return_direction=False, threshold = 0.1 # minimum 'fresh' area left for scanning
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
                    if 1-(end-targetHeight)/targetHeight >= threshold:
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
                    if 1-(end-targetWidth)/targetWidth >=threshold:
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


def resizeImageWithPadding(image, width, height, border_type="constant_black"):
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


from lazero.filesystem import tmpdir, tmpfile

tmpdirPath = "/dev/shm/medialang/nsfw"

import uuid

waitForServerUp(8511, "nsfw nodejs server")
import os

# test_flag = "nsfw"
test_flag = "nsfw_image"
# test_flag = "scanning"
# test_flag = "paddinging"
source = "/root/Desktop/works/pyjom/samples/video/cute_cat_gif.gif"

def processNSFWReportArray(NSFWReportArray, average_classes = ['Neutral'],
            get_max_classes = ['Drawing','Porn','Sexy','Hentai']):
    NSFWReport = {}
    for element in NSFWReportArray:
        for 

# you can reuse this, really.
def NSFWFilter(NSFWReport, _filter={}):


if test_flag == "padding":
    for frame in getVideoFrameIteratorWithFPS(source, -1, -1, fps=1):
        image = resizeImageWithPadding(frame, 1280,720, border_type="replicate")
        # i'd like to view this.
        cv2.imshow("PADDED", image)
        cv2.waitKey(0)
elif test_flag == "scanning":
    for frame in getVideoFrameIteratorWithFPS(source, -1, -1, fps=1):
        scanned_array = scanImageWithWindowSizeAutoResize(frame, 1280, 720, threshold=0.3)
        for index, image in enumerate(scanned_array):
            cv2.imshow("SCANNED %d" % index, image)
            cv2.waitKey(0)
elif test_flag == "nsfw":
    # use another source?
    with tmpdir(path=tmpdirPath) as T:
        for frame in getVideoFrameIteratorWithFPS(source, -1, -1, fps=1):
            padded_resized_frame = resizeImageWithPadding(frame, 224, 224)
            # i'd like to view this.
            basename = "{}.jpg".format(uuid.uuid4())
            jpg_path = os.path.join(tmpdirPath, basename)
            responses = []
            with tmpfile(path=jpg_path) as TF:
                cv2.imwrite(jpg_path, padded_resized_frame)
                files = {"image": (basename, open(jpg_path, "rb"), "image/jpeg")}
                r = requests.post(gateway + "nsfw", files=files)  # post gif? or just jpg?
                response_json = r.json()
                print("RESPONSE:", response_json)
                responses.append(response_json) # there must be at least one response, i suppose?
 # we don't want drawing dogs.

            # [{'className': 'Neutral', 'probability': 0.9995943903923035}, {'className': 'Drawing', 'probability': 0.00019544694805517793}, {'className': 'Porn', 'probability': 0.00013213469355832785}, {'className': 'Sexy', 'probability': 6.839347042841837e-05}, {'className': 'Hentai', 'probability': 9.632151886762585e-06}]
elif test_flag == "nsfw_image":
    source = '/root/Desktop/works/pyjom/samples/image/kitty_flash.bmp'
    # RESPONSE: [{'className': 'Neutral', 'probability': 0.9997681975364685}, {'className': 'Drawing', 'probability': 0.0002115015813615173}, {'className': 'Porn', 'probability': 1.3146535820851568e-05}, {'className': 'Hentai', 'probability': 4.075543984072283e-06}, {'className': 'Sexy', 'probability': 3.15313491228153e-06}]
    # source = '/root/Desktop/works/pyjom/samples/image/pig_really.bmp'
    # RESPONSE: [{'className': 'Neutral', 'probability': 0.9634107351303101}, {'className': 'Porn', 'probability': 0.0244674663990736}, {'className': 'Drawing', 'probability': 0.006115634460002184}, {'className': 'Hentai', 'probability': 0.003590137232095003}, {'className': 'Sexy', 'probability': 0.002416097791865468}]
    # source = "/root/Desktop/works/pyjom/samples/image/dog_with_text.bmp"
    # source = '/root/Desktop/works/pyjom/samples/image/dick2.jpeg'
    # [{'className': 'Porn', 'probability': 0.7400921583175659}, {'className': 'Hentai', 'probability': 0.2109236866235733}, {'className': 'Sexy', 'probability': 0.04403943940997124}, {'className': 'Neutral', 'probability': 0.0034419416915625334}, {'className': 'Drawing', 'probability': 0.0015027812914922833}]
    # source = '/root/Desktop/works/pyjom/samples/image/dick4.jpeg'
    # RESPONSE: [{'className': 'Porn', 'probability': 0.8319052457809448}, {'className': 'Hentai', 'probability': 0.16578854620456696}, {'className': 'Sexy', 'probability': 0.002254955470561981}, {'className': 'Neutral', 'probability': 3.2827374525368214e-05}, {'className': 'Drawing', 'probability': 1.8473130694474094e-05}]
    # source = '/root/Desktop/works/pyjom/samples/image/porn_shemale.jpeg'
    # no good for this one. this is definitely some unacceptable shit, with just cloth wearing.
    # RESPONSE: [{'className': 'Neutral', 'probability': 0.6256022453308105}, {'className': 'Hentai', 'probability': 0.1276213526725769}, {'className': 'Porn', 'probability': 0.09777139872312546}, {'className': 'Sexy', 'probability': 0.09318379312753677}, {'className': 'Drawing', 'probability': 0.05582122132182121}]
    # source ='/root/Desktop/works/pyjom/samples/image/dick3.jpeg'
    # [{'className': 'Porn', 'probability': 0.978420078754425}, {'className': 'Hentai', 'probability': 0.01346961222589016}, {'className': 'Sexy', 'probability': 0.006554164923727512}, {'className': 'Neutral', 'probability': 0.0015426197787746787}, {'className': 'Drawing', 'probability': 1.354961841570912e-05}]
    # a known source causing unwanted shits.
    image = cv2.imread(source)
    basename = "{}.jpg".format(uuid.uuid4())
    jpg_path = os.path.join(tmpdirPath, basename)
    with tmpfile(path=jpg_path) as TF:
        # black padding will lower the probability of being porn.
        padded_resized_frame = resizeImageWithPadding(image, 224, 224)
        # RESPONSE: [{'className': 'Neutral', 'probability': 0.6441782116889954}, {'className': 'Porn', 'probability': 0.3301379978656769}, {'className': 'Sexy', 'probability': 0.010329035110771656}, {'className': 'Hentai', 'probability': 0.010134727694094181}, {'className': 'Drawing', 'probability': 0.005219993181526661}]
        # padded_resized_frame = resizeImageWithPadding(image, 224, 224,border_type='replicate')
        # RESPONSE: [{'className': 'Neutral', 'probability': 0.6340386867523193}, {'className': 'Porn', 'probability': 0.3443007171154022}, {'className': 'Sexy', 'probability': 0.011606302112340927}, {'className': 'Hentai', 'probability': 0.006618513725697994}, {'className': 'Drawing', 'probability': 0.0034359097480773926}]
        # neutral again? try porn!
        cv2.imwrite(jpg_path, padded_resized_frame)
        files = {"image": (basename, open(jpg_path, "rb"), "image/jpeg")}
        r = requests.post(gateway + "nsfw", files=files)  # post gif? or just jpg?
        print("RESPONSE:", r.json())
else:
    raise Exception("unknown test_flag: %s" % test_flag)
# you can only post gif now, or you want to post some other formats?
# if you post shit, you know it will strentch your picture and produce unwanted shits.
