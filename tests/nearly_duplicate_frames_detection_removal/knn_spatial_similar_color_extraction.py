# i'd say i want centrality below 6 percent. what's the catch?

# we'd like to adjust the shift.

# another tip: you have forgot the spatial coordinates.

# fuck!

src = "/root/Desktop/works/pyjom/samples/image/cute_cat.bmp"
# CENTRALITY: 0.00 %

# single not go beyond 4 percent.
# total not go beyond 6 percent.
# is that right? fuck?

# src = "/root/Desktop/works/pyjom/samples/image/dog_with_text.png"
# and yet this does not look right.
# NEARBY CENTER PERCENTAGE: 0.84 %
# CENTRALITY: 2.57 %

# src = "/root/Desktop/works/pyjom/samples/image/miku_on_green.png"
# for this one we have double centers. fuck.
# CENTRALITY: 181.80 %
# it is off the charge!

# with text. a meme.
# src = "/root/Desktop/works/pyjom/samples/image/dog_saturday_night.bmp"
# CENTRALITY: 1.26 %

# src = "/root/Desktop/works/pyjom/samples/image/similar_color_extraction.bmp"  # use some filter first, or rather not to?

# CENTER: [254.62436869 254.63794192 254.79734848]
# POSITIVE COUNT: 188772
# SUM: 566316.0 MIN: 0 MAX: 3
# NEARBY CENTER PERCENTAGE: 81.93 %
# CENTRALITY: 82.33 %

# let's try some cats.

# the filter: removegrain
# src = "/root/Desktop/works/pyjom/samples/image/kitty_flash.bmp"  # use some filter first, or rather not to?
# CENTER: [1.37254902 2.34313725 9.46078431]
# POSITIVE COUNT: 2600
# SUM: 7800.0 MIN: 0 MAX: 3
# NEARBY CENTER PERCENTAGE: 3.91 %
# CENTRALITY: 3.91 %

# now the 八点半配音
# src = "/root/Desktop/works/pyjom/samples/image/is_this_duck.bmp"
# CENTER: [252.66293811 177.62005966 126.37844892]
# POSITIVE COUNT: 222893
# SUM: 668679.0 MIN: 0 MAX: 3
# NEARBY CENTER PERCENTAGE: 36.49 %
# CENTRALITY: 36.55 %
# likely to be the blue.

# src = "/root/Desktop/works/pyjom/samples/image/pig_really.bmp"
# multiple centers.
# CENTER: [246.76865924 226.40763256 216.41472476]
# POSITIVE COUNT: 95497
# SUM: 286491.0 MIN: 0 MAX: 3
# NEARBY CENTER PERCENTAGE: 6.74 %
# CENTRALITY: 7.32 %

import numpy as np
from lazero.utils.importers import cv2_custom_build_init

cv2_custom_build_init()

use_spatial=True

import cv2

image = cv2.imread(src)
shape = image.shape
if len(shape) != 3:
    print("weird shit.")
if shape[2] != 3:
    print("depth not right.")
# for i in range(3):
#     image[:,:,i] = i

if use_spatial:
    col_0, col_1 = shape[:2]

    coords = []

    bias_0 = 2
    bias_1 = 2

    for c0 in range(col_0):
        for c1 in range(col_1):
            coords.append((bias_0*c0/col_0,bias_1*c1/col_1))

    coords = np.array(coords)

# print(image.reshape(-1,3))
reshapedImage = image.reshape(-1, 3)  # are you sure about this?
length, depth = reshapedImage.shape

sample_size_limit = 5000

reshapedImageIndexs = np.arange(0, length)
# so now it is good.
sampleIndexs = np.random.choice(reshapedImageIndexs, size=min(sample_size_limit, length))
print(sampleIndexs)
print(sampleIndexs.shape)

sample_size = len(sampleIndexs)

sample = reshapedImageIndexs[sampleIndexs]
sample = reshapedImage[sample, :]
print(sample)
print(sample.shape)

# breakpoint()
if use_spatial:
    sampleCoords = coords[sampleIndexs]
    sample = np.hstack([sample, sampleCoords])
    print(sample)
    print(sample.shape)
# breakpoint()
# warning: OOM?
# now cluster shit shall we?
# from sklearn.neighbors import NearestNeighbors
# neigh = NearestNeighbors(n_neighbors=5)
# X = sample
# neigh.fit(X)
# A = neigh.kneighbors_graph(X)
# A.toarray()
# print(A)
# print(A.shape) # sparse matrix? wtf?
from sklearn.cluster import MiniBatchKMeans  # better?

# from sklearn.cluster import KMeans
X = sample
batch_size = 45
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

label_percentage = {
    x: np.count_nonzero(labels == x) / sample_size for x in range(n_clusters)
}

flagged_image = image.copy()
flagged_image[:,:,:] = 1 # every element is 1 now.
epsilon = 0.01 # shit man.
percents = []
shift=2
for center5 in cluster_centers:
    # fetch area nearby given center
    if use_spatial:
        center = center5[:3]
    else:
        center = center5
    # center_int = center.astype(np.uint8)
    # i just don't know what the fuck is going on here.
    upper = center + shift
    lower = center - shift
    mask = cv2.inRange(image, lower, upper)
    # not image.
    output = cv2.bitwise_and(flagged_image, flagged_image, mask=mask)
    # print(output)
    # print(output.shape)
    mOutput = output.reshape(-1, 3)
    mOutput = np.sum(mOutput, axis=1)
    mSum = sum(mOutput)
    # breakpoint()
    positive_count = np.count_nonzero(abs(mOutput - 3) < epsilon)
    percent = positive_count/len(mOutput)
    # print(mOutput)
    # print(mOutput.shape)
    # breakpoint()
    print("CENTER:",center)
    print('POSITIVE COUNT:', positive_count)
    print("SUM:", mSum, "MIN:", min(mOutput), 'MAX:', max(mOutput))
    print("NEARBY CENTER PERCENTAGE: {:.2f} %".format(percent*100))
    percents.append(percent)

print("CENTRALITY: {:.2f} %".format(sum(percents)*100))
