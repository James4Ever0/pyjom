from pyjom.medialang.commons import *

import cv2
# import numpy.core.multiarray # caused by numpy version errors. upgrade to resolve.
from videocr import get_subtitles  # are you sure?
import srt
import progressbar


def videoFrameIterator(
    mediapath, timestep=0.5, framebatch=1, data_producer=None, keyword=None
):
    assert data_producer is not None
    assert type(keyword) == str
    assert type(framebatch) == int
    assert framebatch >= 1
    # obviously not for motion detection, if i was saying.
    cap = cv2.VideoCapture(mediapath)
    mdata = []
    fps = cap.get(cv2.CAP_PROP_FPS)
    frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)  # no need of this to get the timecode.
    frames = int(frames)
    # timestep = timestep # unit in seconds.
    if timestep != None:
        frameStep = int(fps * timestep)
    else:
        frameStep = 1 # for None we do frame by frame analysis.
        timestep = 1/fps # generate fake timestep. nothing special.
    assert frameStep > 0
    frameIndex = 0
    # while(cap.isOpened()):
    stepframes = []
    for _ in progressbar.progressbar(range(frames)):
        ret, frame = cap.read()
        if type(frame) != np.ndarray:
            # most likely no thing shown.
            break
        timecode = float(frameIndex / fps)
        if (frameIndex % frameStep) == 0:
            # what is this shit?
            # print("frame:",type(frame))
            # will be replaced!
            stepframes.append(copy.deepcopy(frame))
            if len(stepframes) == framebatch:
                data = data_producer(
                    *stepframes
                )  # usually we treat frames differently?
                stepframes.pop(0)
                # this is part of paddleocr.
                mdata.append(
                    {
                        "time": timecode,
                        "frame": frameIndex,
                        keyword: copy.deepcopy(data),
                    }
                )
        frameIndex += 1
    # result["subtitle_result"]["paddleocr"] = mdata
    cap.release()
    metadata = {"fps": float(fps), "timestep": timestep, "framebatch": framebatch}
    return mdata, metadata
