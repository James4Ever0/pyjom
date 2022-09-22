# USAGE
# python example.py --source images/ocean_sunset.jpg --target images/ocean_day.jpg

# import the necessary packages
from color_transfer import color_transfer
import numpy as np
import argparse
import cv2

def show_image(title, image, width = 300):
	# resize the image to have a constant width, just to
	# make displaying the images take up less screen real
	# estate
	r = width / float(image.shape[1])
	dim = (width, int(image.shape[0] * r))
	resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)

	# show the resized image
	cv2.imshow(title, resized)

def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

# load the images
source = cv2.imread(image_0)
target = cv2.imread(image_1)

# transfer the color distribution from the source image
# to the target image
transfer = color_transfer(source, target, clip=True, preserve_paper=True)


# show the images and wait for a key press
show_image("Source", source)
show_image("Target", target)
show_image("Transfer", transfer)
cv2.waitKey(0)