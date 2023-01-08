from test_commons import *
from pyjom.commons import *
import cv2

import numpy as np


def getBlackPicture(width, height):
    blackPicture = np.zeros((height, width, 3), dtype="uint8")  # this is grayscale.
    return blackPicture


blackPicture = getBlackPicture(500, 500)
cv2.rectangle(blackPicture, (200, 200), (300, 300), (255, 255, 255), 3)
cv2.imshow("image", blackPicture)
cv2.waitKey(0)
