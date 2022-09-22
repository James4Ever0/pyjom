# USAGE
# python example.py --source images/ocean_sunset.jpg --target images/ocean_day.jpg

image_0 = ""
image_1 = ""

from lazero.utils.importers import cv2_custom_build_init
cv2_custom_build_init()

# import the necessary packages
from color_transfer import color_transfer
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

# load the images
source = cv2.imread(image_0)
target = cv2.imread(image_1)

# transfer the color distribution from the source image
# to the target image
transfer = color_transfer(source, target)


transfer_02 = source*0.8+transfer*0.2

# show the images and wait for a key press
show_image("Source", source)
show_image("Target", target)
show_image("Transfer", transfer)
cv2.waitKey(0)