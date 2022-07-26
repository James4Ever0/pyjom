from reloading import reloading
from .mediaDetector import *


@reloading
def frameDifferential(frame_a, frame_b, cut=3, absolute=True, method="average"):
    assert cut >= 1
    # calculate average difference.
    # you can select ROI instead.
    # the cut is generated by the smallest side. neglect the boundary.
    mshape = frame_a.shape
    width, height = mshape[:2]
    mcut = int(min(width, height) / cut)
    result = frame_a - frame_b
    methods = {"average": np.average, "max": np.max, "min": np.min}
    # it is hard to tell where the heck does the target go. since the color difference means nothing precisely.
    # maybe you should mark the target for us? for our training model?
    # and again use our superduper unet? you know sometimes we get static.
    # so use both inputs. one for static and one for motion.
    if absolute:
        result = np.abs(result)
    if len(mshape) == 3:
        result = methods[method](result, axis=2)  # just np.max
        # i guess it is about the max value not the unified.
    shape0 = int(width / mcut)
    shape1 = int(height / mcut)
    diff = np.zeros((shape0, shape1)).tolist()
    # mapping = {}
    for x in range(shape0):
        for y in range(shape1):
            diff[x][y] = float(
                np.average(result[x * mcut : (x + 1) * mcut, y * mcut : (y + 1) * mcut])
            )
            # this mapping is bad.
            # mapping.update({str((x,y)):((x*mcut,(x+1)*mcut),(y*mcut,(y+1)*mcut))})
    return {"diff": diff, "blocksize": mcut}  # required for recovering center points.
    # transform the frames into smaller matricies.
    # not required all the time though.


@reloading
def videoDiffDetector(mediapaths, cut=3, absolute=True, method="average", timestep=0.2):
    # any better detectors? deeplearning?
    results = []
    data_key = "diff_result"
    for mediapath in mediapaths:
        print("mediapath:", mediapath)
        mediatype = getFileType(mediapath)
        print("subtitle of mediatype:", mediatype)
        assert mediatype in ["video"]  # gif? anything like that?
        result = {"type": mediatype, data_key: {}}
        config = {"cut": cut, "absolute": absolute, "method": method}
        keyword = "frame_differential"
        mdata, metadata = videoFrameIterator(
            mediapath,
            data_producer=keywordDecorator(frameDifferential, **config),
            framebatch=2,
            timestep=timestep,
            keyword=keyword,
        )
        metadata.update({"config": config})
        result[data_key][keyword] = mdata
        result[data_key].update(metadata)
        results.append(result)
    return results
