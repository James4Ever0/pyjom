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

def resizeWithPadding(image, width, height):
    cv2.resize(image, (targetwidth, targetHeight), interpolation=cv2.INTER_CUBIC)

from lazero.filesystem import tmpdir

r = requests.post(gateway,) # post gif?
# you can only post gif now, or you want to post some other formats?
# if you post shit, you know it will strentch your picture and produce unwanted shits.