# we take max for the concerned ones, and take mean for the unconcerned ones.

from test_commons import *
import requests
from lazero.network.checker import waitForServerUp
from pyjom.videotoolbox import getVideoFrameIteratorWithFPS

gateway = "http://localhost:8080/"
source = "/root/Desktop/works/pyjom/samples/video/cute_cat_gif.gif"

from lazero.utils.importers import cv2_custom_build_init

cv2_custom_build_init()
import cv2

# suggest you not to use this shit.
import math

def scanImageWithWindowSize(image, width, height, return_direction=False):
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
    if targetWidth/targetHeight == width/height:
        imageSeries = [resized] # as image series.
        direction = None
    elif targetWidth/targetHeight < width/height:
        direction = ""
    else:
        direction = 
    return imageSeries, direction

def resizeImageWithPadding(image, width, height):
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
    padded = cv2.copyMakeBorder(
        resized, top, bottom, left, right, cv2.BORDER_CONSTANT, value=BLACK
    )
    return padded


from lazero.filesystem import tmpdir

tmpdirPath = "/dev/shm/medialang/nsfw"


r = requests.post(
    gateway,
)  # post gif?
# you can only post gif now, or you want to post some other formats?
# if you post shit, you know it will strentch your picture and produce unwanted shits.
