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


def scanImageWithWindowSizeAutoResize(image, width, height, return_direction=False): # shall you use torch? no?
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
    targetWidth = min(width, min(math.floor(iw * height / ih)))
    targetHeight = min(height, min(math.floor(ih * width / iw)))
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

waitForServerUp(8511,"")

with tmpdir(path=tmpdirPath) as T:
    for frame in getVideoFrameIteratorWithFPS(source, -1, -1, fps=1):
        padded_resized_frame = resizeImageWithPadding(frame, 224, 224)
        jpg_path = os.path.join(tmpdirPath, "{}.jpg".format(uuid.uuid4()))
        with tmpfile(path=jpg_path) as TF:
            cv2.imwrite(jpg_path, padded_resized_frame)
            r = requests.post(
                gateway+"nsfw",
            )  # post gif? or just jpg?
# you can only post gif now, or you want to post some other formats?
# if you post shit, you know it will strentch your picture and produce unwanted shits.
