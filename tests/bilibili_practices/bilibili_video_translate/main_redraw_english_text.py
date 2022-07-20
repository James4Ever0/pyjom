from paddleocr import PaddleOCR

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
prob_thresh = 0.6 # found watermark somewhere. scorpa
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

# from PIL import Image
from PIL import Image, ImageFont, ImageDraw  

def np2pillow(opencv_image):
    color_coverted = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(color_coverted)
    return pil_image
    # pil_image.show()

def pillow2np(pil_image):
    # pil_image=Image.open("demo2.jpg") # open image using PIL
    # use numpy to convert the pil_image into a numpy array
    numpy_image=np.array(pil_image)  
    # convert to a openCV2 image, notice the COLOR_RGB2BGR which means that 
    # the color is converted from RGB to BGR format
    opencv_image=cv2.cvtColor(numpy_image, cv2.COLOR_RGB2BGR) 
    return opencv_image
# draw text now!
mpil_image = np2pillow(dst)
draw = ImageDraw.Draw(mpil_image)
font_location = "/root/Desktop/works/bilibili_tarot/SimHei.ttf" # not usual english shit.


def get_coord_orientation_font_size_and_center(coords):
    xlist, ylist = [x[0] for x in coords], [x[1] for x in coords]
    min_x, max_x = min(xlist), max(xlist)
    min_y, max_y = min(ylist), max(ylist)
    width,height = max_x-min_x, max_y-min_y
    center = (int((max_x+min_x)/2),int((max_y+min_y)/2))
    # what about rotation? forget about it...
    if (width / height) < 0.8:
        orientation = "vertical"
        font_size = int(width)
    else:
        orientation = "horizontal"
        font_size = int(height)
    return orientation, font_size, center,(width,height)

readjust_size=True
comparedWaterMarkString = "scorpa".lower() # the freaking name 
comparedWaterMarkStringLength = len(comparedWaterMarkString)
import Levenshtein

for coords, (text,prob) in result:
    # remove watermarks? how to filter?
    editDistanceThreshold = 4
    probThreshold = 0.8
    textCompareCandidate = text.replace(" ","").lower()
    distance = Levenshtein.distance(textCompareCandidate,comparedWaterMarkString)
    string_length = len(text)
    string_length_difference = abs(string_length-comparedWaterMarkStringLength)
    length_difference_threshold = 3
    if (distance < editDistanceThreshold and string_length_difference < length_difference_threshold) or prob < probThreshold:
        continue # skip all shits.
    # specified font size 
    orientation, font_size, center ,(width,height) = get_coord_orientation_font_size_and_center(coords)
    if orientation == "horizontal":
        font = ImageFont.truetype(font_location, font_size)
        # text = original_text
        # drawing text size 
        stroke_width = int(0.1*font_size)
        (string_width,string_height) = draw.textsize(text,font=font,stroke_width=stroke_width)
        # print(string_width)
        # breakpoint()
        if readjust_size:
            change_ratio = width/string_width
            new_fontsize = font_size*change_ratio
            font = ImageFont.truetype(font_location, new_fontsize)
            start_x = int(center[0]-width/2)
            start_y = int(center[1]-height/2)
        else:
            start_x = int(center[0]-string_width/2)
            start_y = int(center[1]-font_size/2)
        draw.text((start_x, start_y), text, font = font, fill=(255,255,255),stroke_fill=(0,0,0),stroke_width = stroke_width,align ="left") # what is the freaking align?
    
# mpil_image.show() 
mpil_image.save("redraw_english.png")
# cv2.imshow('dst',dst2)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

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