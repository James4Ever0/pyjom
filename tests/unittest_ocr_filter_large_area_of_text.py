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



    for index, frame in enumerate(iterator):
        if noWHInfo:
            noWHInfo = False
            height, width = frame.shape[:2]
        detection, recognition = reader.detect(frame)  # not very sure.
        if detection == [[]]:
            detectionList.append([])
            continue
        # print("frame number:",index)
        # for boundingBox in detection[0]:
        #     print(boundingBox) # left, right, top, bottom

        detectionList.append([LRTBToDiagonal(x) for x in detection[0]].copy())
for img in iterator:
    # d = pytesseract.image_to_data(img, output_type=Output.DICT)
    n_boxes = len(d['level'])
    for i in range(n_boxes):
        (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow('img', img)
    cv2.waitKey(0)