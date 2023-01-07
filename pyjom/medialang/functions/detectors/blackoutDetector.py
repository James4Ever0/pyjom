from .mediaDetector import *


def blackoutIdentifier(frame_a, cut=3, threshold=30, method="average"):
    assert cut >= 1
    methods = {"average": np.average, "max": np.max, "min": np.min}
    mshape = frame_a.shape
    width, height = mshape[:2]
    mcut = int(min(width, height) / cut)
    if len(mshape) == 3:
        result = methods[method](result, axis=2)
        shape0 = int(width / mcut)
    shape1 = int(height / mcut)
    diff = np.zeros((shape0, shape1)).tolist()
    # mapping = {}
    for x in range(shape0):
        for y in range(shape1):
            area = result[x * mcut : (x + 1) * mcut, y * mcut : (y + 1) * mcut]
            score = (area < threshold).astype(int)
            diff[x][y] = score.sum() / score.size
    return {
        "blackout": diff,
        "blocksize": mcut,
    }  # required for recovering center points.


def blackoutDetector(mediapaths, cut=3, threshold=30, method="average", timestep=0.2):
    # any better detectors? deeplearning?
    results = []
    data_key = "blackout_score"
    for mediapath in mediapaths:
        print("mediapath:", mediapath)
        mediatype = getFileType(mediapath)
        print("subtitle of mediatype:", mediatype)
        assert mediatype in ["video", "image"]  # gif? anything like that?
        result = {"type": mediatype, data_key: {}}
        config = {"cut": cut, "threshold": threshold, "method": method}

        if mediatype == "image":
            data = cv2.imread(mediapath)
            data = keywordDecorator(blackoutIdentifier, **config)(data)
            result[data_key].update({"blackout_detector": data})
            result[data_key].update({"config": config})
        else:
            keyword = "blackout_detector"
            mdata, metadata = videoFrameIterator(
                mediapath,
                data_producer=keywordDecorator(blackoutIdentifier, **config),
                framebatch=1,
                timestep=timestep,
                keyword=keyword,
            )
            metadata.update({"config": config})
            result[data_key][keyword] = mdata
            result[data_key].update(metadata)
        results.append(result)
    return results
