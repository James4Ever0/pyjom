from test_commons import *

import pytesseract
from pytesseract import Output
from lazero.utils.importers import cv2_custom_build_init
cv2_custom_build_init()
# import cv2
# img = cv2.imread('image.jpg')
from pyjom.videotoolbox import getVideoFrameIteratorWithFPS

iterator = getVideoFrameIteratorWithFPS(videoPath, start=-1, end=-1, fps=)

d = pytesseract.image_to_data(img, output_type=Output.DICT)
n_boxes = len(d['level'])
for i in range(n_boxes):
    (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

cv2.imshow('img', img)
cv2.waitKey(0)