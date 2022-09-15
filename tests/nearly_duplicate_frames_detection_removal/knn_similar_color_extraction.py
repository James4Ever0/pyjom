src = "/root/Desktop/works/pyjom/samples/image/similar_color_extraction.bmp" # use some filter first, or rather not to?

import numpy as np
from lazero.utils.importers import cv2_custom_build_init
cv2_custom_build_init()

import cv2
# from sklearn.cluster import KMeans

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

reshapedImageIndexs = np.arange(0, length)
# so now it is good.
sample = np.random.choice(reshapedImageIndexs,size=min(5000, length))
print(sample)
print(sample.shape)

sample = reshapedImage[sample,:]
print(sample)
print(sample.shape)

# now cluster shit shall we?
from sklearn.neighbors import NearestNeighbors
neigh = NearestNeighbors(n_neighbors=5)
X = sample
neigh.fit(X)
A = neigh.kneighbors_graph(X)
A.toarray()
print(A)
print(A.shape) # sparse matrix? wtf?