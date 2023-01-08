from test_commons import *

# import pytesseract
# from pytesseract import Output
from lazero.utils.importers import cv2_custom_build_init

cv2_custom_build_init()
import cv2

# img = cv2.imread('image.jpg')
from pyjom.videotoolbox import getVideoFrameIteratorWithFPS


detectionList = []
from pyjom.imagetoolbox import getEasyOCRReader, LRTBToDiagonal

reader = getEasyOCRReader(("en",))

import numpy as np

test_subject = "image"

if test_subject == "video":
    videoPath = "/root/Desktop/works/pyjom/samples/video/dog_with_large_text.gif"
    iterator = getVideoFrameIteratorWithFPS(videoPath, start=-1, end=-1, fps=10)
elif test_subject == "image":
    imagePath = "/root/Desktop/works/pyjom/samples/image/dog_saturday_night.bmp"
    iterator = [cv2.imread(imagePath)]
else:
    raise Exception("unknown test_subject:", test_subject)

# threshold: {'max':0.3}
for frame in iterator:
    height, width = frame.shape[:2]
    img = np.zeros((height, width, 3))
    detection, recognition = reader.detect(frame)  # not very sure.
    if detection == [[]]:
        diagonalRects = []
    else:
        diagonalRects = [LRTBToDiagonal(x) for x in detection[0]]
    for x1, y1, x2, y2 in diagonalRects:
        w, h = x2 - x1, y2 - y1
        x, y = x1, y1
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), -1)
    # calculate the portion of the text area.
    textArea = np.sum(img)
    textAreaRatio = (textArea / 255) / (width * height)
    print("text area: {:.2f} %".format(textAreaRatio))
    cv2.imshow("img", img)
    cv2.waitKey(0)
