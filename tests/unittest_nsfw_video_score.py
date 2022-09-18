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
def resizeWithPadding(image, width, height):
    shape = image.shape
    assert len(shape) == 3
    ih, iw, channels = shape
    targetWidth = min(width, min(math.floor(iw*height/ih)))
    targetHeight =  min(height, min(math.floor(ih*width/iw)))
    resized = cv2.resize(image, (targetWidth, targetHeight), interpolation=cv2.INTER_CUBIC)
    BLACK = [0]*channels
    top = max(0,math.floor((height-targetHeight)/2))
    bottom = max(0,targetHeight-top)
    left = max(0,math.floor((width-targetWidth)/2))
    right = max(0,targetWidth-left)
    cv2.copyMakeBorder(resized,top, bottom, left, right,cv2.BORDER_CONSTANT , value=BLACK)

from lazero.filesystem import tmpdir

r = requests.post(gateway,) # post gif?
# you can only post gif now, or you want to post some other formats?
# if you post shit, you know it will strentch your picture and produce unwanted shits.