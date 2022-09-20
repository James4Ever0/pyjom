from test_commons import *

# import pytesseract
# from pytesseract import Output
from lazero.utils.importers import cv2_custom_build_init
cv2_custom_build_init()
import cv2
# img = cv2.imread('image.jpg')
from pyjom.videotoolbox import getVideoFrameIteratorWithFPS

# videoPath = "/root/Desktop/works/pyjom/samples/video/dog_with_large_text.gif"
# check another video?
videoPath = "/root/Desktop/works/pyjom/samples/video/cute_cat_gif.mp4"

iterator = getVideoFrameIteratorWithFPS(videoPath, start=-1, end=-1, fps=10)

detectionList = []
from pyjom.imagetoolbox import getEasyOCRReader, LRTBToDiagonal
reader = getEasyOCRReader(['en'])

import numpy as np
for frame in iterator:
    img = np.zeros(height, width, 3)
    height, width = frame.shape[:2]
    detection, recognition = reader.detect(frame)  # not very sure.
    if detection == [[]]:
        diagonalRects = []
    else:
        diagonalRects = [LRTBToDiagonal(x) for x in detection[0]]
    for x1, y1, x2, y2 in diagonalRects:
        w,h = x2-x1, y2-y1
        x,y = x1,y1
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), -1)

    cv2.imshow('img', img)
    cv2.waitKey(0)