from test_commons import *
from pyjom.commons import *
import cv2

import numpy as np

def getBlackPicture(width, height):
    blackPicture =  np.zeros((height, width,3), dtype = "uint8") # this is grayscale.
    return blackPicture

blackPicture = getBlackPicture(500,500)
