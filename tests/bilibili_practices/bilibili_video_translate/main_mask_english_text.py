from paddleocr import PaddleOCR,draw_ocr

# cannot translate everything... not frame by frame...

# can summarize things. can block texts on location.

# Paddleocr supports Chinese, English, French, German, Korean and Japanese.
# You can set the parameter `lang` as `ch`, `en`, `french`, `german`, `korean`, `japan`
# to switch the language model in order.
ocr = PaddleOCR(use_angle_cls=True, lang='en') # need to run only once to download and load model into memory
img_path = 'target.png' # only detect english. or not?


import cv2

image = cv2.imread(img_path)

result2 = ocr.ocr(image, cls=True)
prob_thresh = 0.8
result = []

import wordninja
for index, line in enumerate(result2):
    # print(line)
    # breakpoint()
    coords, (text, prob) = line
    prob = float(prob)
    if prob > prob_thresh:
        rectified_text = " ".join(wordninja.split(text))
        line[1] = (rectified_text, prob)
        print(line)
        result.append(line)

import numpy as np

a,b,c = image.shape

blank_image = np.zeros(shape=[a,b], dtype=np.uint8) # the exact order

for coords, (text,prob) in result:
    polyArray = np.array(coords).astype(np.int64) # fuck.
    # print(polyArray)
    # print(polyArray.shape)
    # breakpoint()
    # points = np.array([[160, 130], [350, 130], [250, 300]])
    # print(points.dtype)
    # points = np.array([[454.0, 22.0], [464.0, 26.0], [464.0, 85.0]]).astype(np.int64)
    color= 255
    cv2.fillPoly(blank_image,[polyArray],color)
    isClosed = True
    thickness = 30
    cv2.polylines(blank_image, [polyArray], isClosed, color, thickness) # much better.
#     # cv2.fillPoly(blank_image,pts=[points],color=(255, 255,255))
# cv2.imshow("mask",blank_image)
# cv2.waitKey(0)
# use wordninja.
# before translation we need to lowercase these shits.
dst = cv2.inpaint(image,blank_image,3,cv2.INPAINT_TELEA)
cv2.imshow('dst',dst)
cv2.waitKey(0)
cv2.destroyAllWindows()

# expand the area somehow.
# draw result
# simhei_path = "/root/Desktop/works/bilibili_tarot/SimHei.ttf"
# from PIL import Image
# image = Image.open(img_path).convert('RGB')
# boxes = [line[0] for line in result]
# txts = [line[1][0] for line in result]
# scores = [line[1][1] for line in result]
# im_show = draw_ocr(image, boxes, txts, scores, font_path=simhei_path)
# im_show = Image.fromarray(im_show)
# im_show.save('result.jpg')

# we will be testing one image only. not the whole goddamn video.
# may have cuda error when using my cv2 cuda libs.