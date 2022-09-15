src = "/root/Desktop/works/pyjom/samples/image/similar_color_extraction.bmp" # use some filter first, or rather not to?

import numpy as np
from lazero.utils.importers import cv2_custom_build_init
cv2_custom_build_init()

import cv2

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

sample_size_limit = 5000

reshapedImageIndexs = np.arange(0, length)
# so now it is good.
sample = np.random.choice(reshapedImageIndexs,size=min(sample_size_limit, length))
print(sample)
print(sample.shape)

sample_size = len(sample)

sample = reshapedImage[sample,:]
print(sample)
print(sample.shape)

# now cluster shit shall we?
# from sklearn.neighbors import NearestNeighbors
# neigh = NearestNeighbors(n_neighbors=5)
# X = sample
# neigh.fit(X)
# A = neigh.kneighbors_graph(X)
# A.toarray()
# print(A)
# print(A.shape) # sparse matrix? wtf?
from sklearn.cluster import MiniBatchKMeans # better?
# from sklearn.cluster import KMeans
X = sample
batch_size=45
# kmeans = KMeans(n_clusters=5).fit(X) # not deterministic please?
n_clusters = 5
kmeans = MiniBatchKMeans(
    init="k-means++",
    n_clusters=n_clusters,
    batch_size=batch_size,
    # n_init=10,
    max_no_improvement=10,
    verbose=0,
).fit(X)
# from lazero.utils import inspectObject
# inspectObject(kmeans)
# breakpoint()
labels = kmeans.labels_
cluster_centers = kmeans.cluster_centers_
print(labels)
print(cluster_centers)

label_percentage = {x: labels.count(x)/sample_size for x in range(n_clusters)}

for center in cluster_centers:
    # fetch area nearby given center