src = "/root/Desktop/works/pyjom/samples/image/similar_color_extraction.bmp" # use some filter first, or rather not to?

import numpy as np
from lazero.utils.importers import cv2_custom_build_init
cv2_custom_build_init()

import cv2
from sklearn.cluster import KMeans

image = cv2.imread(src)
# for i in range(3):
#     image[:,:,i] = i

# print(image.reshape(-1,3))
