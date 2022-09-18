# we take max for the concerned ones, and take mean for the unconcerned ones.

from test_commons import *
import requests
from lazero.network.checker import waitForServerUp
from pyjom.videotoolbox import getVideoFrameIteratorWithFPS

gateway = "http://localhost:8511/"
source = "/root/Desktop/works/pyjom/samples/video/cute_cat_gif.gif"

from lazero.utils.importers import cv2_custom_build_init

cv2_custom_build_init()
import cv2

# suggest you not to use this shit.
import math


def scanImageWithWindowSizeAutoResize(
    image, width, height, return_direction=False
):  # shall you use torch? no?
    shape = image.shape
    assert len(shape) == 3
    ih, iw, channels = shape
    targetWidth = max(width, min(math.floor(iw * height / ih)))
    targetHeight = max(height, min(math.floor(ih * width / iw)))
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
                    end = targetHeight
                    start = targetHeight - height
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
                    end = targetWidth
                    start = targetWidth - width
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

test_flag = ""

if test_flag == "":
elif test_flag == "nsfw":
    with tmpdir(path=tmpdirPath) as T:
        for frame in getVideoFrameIteratorWithFPS(source, -1, -1, fps=1):
            padded_resized_frame = resizeImageWithPadding(frame, 224, 224)
            # i'd like to view this.
            basename = "{}.jpg".format(uuid.uuid4())
            jpg_path = os.path.join(tmpdirPath, basename)
            with tmpfile(path=jpg_path) as TF:
                cv2.imwrite(jpg_path, padded_resized_frame)
                files = {"image": (basename, open(jpg_path, "rb"), "image/jpeg")}
                r = requests.post(gateway + "nsfw", files=files)  # post gif? or just jpg?
                print("RESPONSE:", r.json())
            # [{'className': 'Neutral', 'probability': 0.9995943903923035}, {'className': 'Drawing', 'probability': 0.00019544694805517793}, {'className': 'Porn', 'probability': 0.00013213469355832785}, {'className': 'Sexy', 'probability': 6.839347042841837e-05}, {'className': 'Hentai', 'probability': 9.632151886762585e-06}]
else:
    raise Exception("unknown test_flag: %s" % test_flag)
# you can only post gif now, or you want to post some other formats?
# if you post shit, you know it will strentch your picture and produce unwanted shits.
