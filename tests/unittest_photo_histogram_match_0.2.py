# USAGE
# python example.py --source images/ocean_sunset.jpg --target images/ocean_day.jpg

image_0 = "/root/Desktop/works/pyjom/samples/image/dog_with_text2.png"
image_1 = "/root/Desktop/works/pyjom/samples/image/cute_cat.bmp"

# from lazero.utils.importers import cv2_custom_build_init
from test_commons import *

# cv2_custom_build_init()

# import the necessary packages
from color_transfer import color_transfer
import cv2


def show_image(title, image, width=300):
    # resize the image to have a constant width, just to
    # make displaying the images take up less screen real
    # estate
    r = width / float(image.shape[1])
    dim = (width, int(image.shape[0] * r))
    resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

    # show the resized image
    cv2.imshow(title, resized)


# load the images
source = cv2.imread(image_0)
target = cv2.imread(image_1)


# we inpaint this one from the beginning.
from pyjom.imagetoolbox import (
    getImageTextAreaRatio,
    imageFourCornersInpainting,
)  # also for image text removal.

target = getImageTextAreaRatio(target, inpaint=True)
target = imageFourCornersInpainting(target)
# also remove the selected area.

# transfer the color distribution from the source image
# to the target image
transfer = color_transfer(source, target)

import numpy as np

transfer_02 = (target * 0.8 + transfer * 0.2).astype(np.uint8)

transfer_02_flip = cv2.flip(transfer_02, 1)

# show the images and wait for a key press
show_image("Source", source)
show_image("Target", target)
show_image("Transfer", transfer)
show_image("Transfer_02", transfer_02)
show_image("Transfer_02_flip", transfer_02_flip)
cv2.waitKey(0)
