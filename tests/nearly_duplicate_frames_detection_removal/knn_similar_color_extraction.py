src = "/root/Desktop/works/pyjom/samples/image/similar_color_extraction.bmp" # use some filter first, or rather not to?

import numpy as np
from lazero.utils.importers import cv2_custom_build_init
cv2_custom_build_init()

import cv2
from sklearn.cluster import KMeans

image = cv2.imread(src)
shape = image.shape
if len(shape) !=3:
    print('weird shit.')
if shape[2] !=3:
    print("depth not right.")
# for i in range(3):
#     image[:,:,i] = i

# print(image.reshape(-1,3))
reshapedImage = image.reshape(-1,3) # are you sure about this?
length, depth = reshapedImage.shape

np.arange(0, length)
# so now it is good.
sample = np.random.choice(reshapedImage,size=min(5000, length))
print(sample)
print(sample.shape)