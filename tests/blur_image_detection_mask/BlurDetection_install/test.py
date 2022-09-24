# order:
# detect if dog/cat is there, satisfying the qualification
# remove watermark, remove text, remove potential watermark around corners using inpainting
# use ffmpeg cropdetect, if has significant area change then no further processing
# if no significant area change, use this blur detection to get the main area
# remove watermark again?? around corners?
# then reuse the dog detection and get the crop from processed/cropped image.

import os

# from cv2 import waitKey
from lazero.utils.importers import cv2_custom_build_init

cv2_custom_build_init()
import cv2
import numpy

# import logger
import BlurDetection

# img_path = raw_input("Please Enter Image Path: ")
# img_path = "/root/Desktop/works/pyjom/samples/image/dog_blue_sky_split_line.png"
# img_path = "/root/Desktop/works/pyjom/samples/image/blur_sample.webp"
img_path = "/root/Desktop/works/pyjom/samples/image/blur_sample_2.webp"

# img_path = "/root/Desktop/works/pyjom/samples/image/dog_with_black_borders.png"

# ffmpeg -loop 1 -i /root/Desktop/works/pyjom/samples/image/dog_with_black_borders.png -t 15 -vf cropdetect -f null -
# img_path="/root/Desktop/works/pyjom/samples/image/husky_cry.png"
assert os.path.exists(img_path), "img_path does not exists"
img = cv2.imread(img_path)

import sys

sys.path.append("/root/Desktop/works/pyjom/")
from pyjom.imagetoolbox import imageFourCornersInpainting, getImageTextAreaRatio

img = imageFourCornersInpainting(img)
img = getImageTextAreaRatio(img, inpaint=True, edgeDetection=True)

img_fft, val, blurry = BlurDetection.blur_detector(img)
print("this image {0} blurry".format(["isn't", "is"][blurry]))
msk, result, blurry = BlurDetection.blur_mask(img, max_thresh=120)

inv_msk = 255 - msk
# import numpy as np
# print(np.max(msk), np.min(msk))
# print(msk.shape)
# breakpoint()


def display(title, img, max_size=200000):
    assert isinstance(img, numpy.ndarray), "img must be a numpy array"
    assert isinstance(title, str), "title must be a string"
    scale = numpy.sqrt(min(1.0, float(max_size) / (img.shape[0] * img.shape[1])))
    print("image is being scaled by a factor of {0}".format(scale))
    shape = (int(scale * img.shape[1]), int(scale * img.shape[0]))
    img = cv2.resize(img, shape)
    cv2.imshow(title, img)


# BlurDetection.scripts.display('img', img)
display("img", img)
# display("msk", msk)
display("inv_msk", inv_msk)
# Generate contours based on our mask
# This function allows us to create a descending sorted list of contour areas.

# def contour_area(contours):

#     # create an empty list
#     cnt_area = []

#     # loop through all the contours
#     for i in range(0, len(contours), 1):
#         # for each contour, use OpenCV to calculate the area of the contour
#         cnt_area.append(cv2.contourArea(contours[i]))

#     # Sort our list of contour areas in descending order
#     list.sort(cnt_area, reverse=True)
#     return cnt_area


def draw_bounding_box_with_contour(
    contours, image, area_threshold=20, debug=False
):  # are you sure?
    # this is the top-k approach.
    # Call our function to get the list of contour areas
    # cnt_area = contour_area(contours)

    # Loop through each contour of our image
    x0, y0, x1, y1 = [None] * 4
    for i in range(0, len(contours), 1):
        cnt = contours[i]
        # Only draw the the largest number of boxes
        if cv2.contourArea(cnt) > area_threshold:
            # if (cv2.contourArea(cnt) > cnt_area[number_of_boxes]):

            # Use OpenCV boundingRect function to get the details of the contour
            x, y, w, h = cv2.boundingRect(cnt)
            if x0 == None:
                x0, y0, x1, y1 = x, y, x + w, y + h
            if x < x0:
                x0 = x
            if y < y0:
                y0 = y
            if x + w > x1:
                x1 = x + w
            if y + h > y1:
                y1 = y + h
            # Draw the bounding box

    if x0 is not None:
        if debug:
            image = cv2.rectangle(image, (x0, y0), (x1, y1), (0, 0, 255), 2)
            cv2.imshow("with_bounding_box", image)
            cv2.waitKey(0)

    if x0 is None:
        height, width = image.shape[:2]
        x0, y0, x1, y1 = 0, 0, width, height
    return (x0, y0), (x1, y1)


# BlurDetection.scripts.display('msk', msk)
contours, hierarchy = cv2.findContours(inv_msk, 1, 2)
rectangle_boundingbox = draw_bounding_box_with_contour(contours, img, debug=True)
# cv2.waitKey(0)
