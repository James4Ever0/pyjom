from pyjom.commons import *
import numpy as np

def getColorCentrality(image,sample_size_limit = 5000,
    epsilon = 0.01, # shit man.
    shift=2,
    n_clusters = 5,
    batch_size = 45,
    max_no_improvement=10,
):
    # image is of numpy.array
    # multiple centers.
    # CENTER: [246.76865924 226.40763256 216.41472476]
    # POSITIVE COUNT: 95497
    # SUM: 286491.0 MIN: 0 MAX: 3
    # NEARBY CENTER PERCENTAGE: 6.74 %
    # CENTRALITY: 7.32 %
    import cv2
    # image = cv2.imread(src)
    shape = image.shape
    if len(shape) != 3:
        print("weird shit.")
        breakpoint()
    if shape[2] != 3:
        print("depth not right.")
        breakpoint()
    # for i in range(3):
    #     image[:,:,i] = i

    # col_0, col_1 = shape[:2]

    # coords = []

    # for c0 in range(col_0):
    #     for c1 in range(col_1):
    #         coords.append((c0,c1))

    # coords = np.array(coords)

    # print(image.reshape(-1,3))
    reshapedImage = image.reshape(-1, 3)  # are you sure about this?
    length, color_channels= reshapedImage.shape


    reshapedImageIndexs = np.arange(0, length)
    # so now it is good.
    sampleIndexs = np.random.choice(reshapedImageIndexs, size=min(sample_size_limit, length))
    # print(sampleIndexs)
    # print(sampleIndexs.shape)

    sample_size = len(sampleIndexs)

    sample = reshapedImageIndexs[sampleIndexs]
    sample = reshapedImage[sample, :]
    # print(sample)
    # print(sample.shape)

    # breakpoint()
    # sampleCoords = coords[sampleIndexs]
    # sample = np.hstack([sample, sampleCoords])
    # print(sample)
    # print(sample.shape)
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
    # kmeans = KMeans(n_clusters=5).fit(X) # not deterministic please?
    kmeans = MiniBatchKMeans(
        init="k-means++",
        n_clusters=n_clusters,
        batch_size=batch_size,
        # n_init=10,
        max_no_improvement=max_no_improvement,
        verbose=0,
    ).fit(X)
    # from lazero.utils import inspectObject
    # inspectObject(kmeans)
    # breakpoint()
    labels = kmeans.labels_
    cluster_centers = kmeans.cluster_centers_
    # print(labels)
    # print(cluster_centers)

    label_percentage = {
        x: np.count_nonzero(labels == x) / sample_size for x in range(n_clusters)
    }

    flagged_image = image.copy()
    flagged_image[:,:,:] = 1 # every element is 1 now.
    percents = []
    for center in cluster_centers:
        # fetch area nearby given center
        # center = center5[:3]
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
        # print("CENTER:",center)
        # print('POSITIVE COUNT:', positive_count)
        # print("SUM:", mSum, "MIN:", min(mOutput), 'MAX:', max(mOutput))
        # print("NEARBY CENTER PERCENTAGE: {:.2f} %".format(percent*100))
        percents.append(percent)
    max_nearby_center_percentage = max(percents)
    print("NEARBY CENTER PERCENTAGE: {:.2f} %".format(max_nearby_center_percentage*100))
    centrality=sum(percents)
    print("CENTRALITY: {:.2f} %".format(centrality*100))
    return centrality, max_nearby_center_percentage
