# videoLink = "https://www.bilibili.com/video/BV1Cb4y1s7em" # this is a dog.

videoLink = "https://www.bilibili.com/video/BV1Lx411B7X6" # multipart download

from lazero.filesystem.temp import tmpfile

import yt_dlp
# import pyidm

path = "/dev/shm/testVideo.mp4"
from test_commons import *
import cv2
from pyjom.videotoolbox import getVideoFrameSampler
from pyjom.imagetoolbox import bezierPaddleHubResnet50ImageDogCatDetector, getImageTextAreaRatio, imageFourCornersInpainting
from pyjom.commons import checkMinMaxDict

dog_or_cat = "dog"
confidence_threshold = {"min":0.7}
text_area_threshold = {"max":0.2}

with tmpfile(path=path, replace=True) as TF:
    x = yt_dlp.YoutubeDL({"outtmpl":path,})
    y = x.download([videoLink])
# shall you use frame sampler instead of iterator? cause this is dumb.
    breakpoint()
    from caer.video.frames_and_fps import get_duration
    duration = get_duration(path)
    mSampleSize = int(duration/2) # fps = 0.5 or something?
    processed_frame = None
    for frame in getVideoFrameSampler(path, -1,-1,sample_size=mSampleSize,iterate=True):
        text_area_ratio = getImageTextAreaRatio(frame)
        if checkMinMaxDict(text_area_ratio,text_area_threshold):
            detections = bezierPaddleHubResnet50ImageDogCatDetector(frame)
            mDetections = [x for x in detections if x['identity'] == dog_or_cat]
            mDetections.sort(key=lambda x: -x['confidence']) # select the best one.
            if len(mDetections)>0:
                best_confidence = mDetections[0]['confidence']
                if checkMinMaxDict(best_confidence, confidence_threshold):
                    target = getImageTextAreaRatio(frame, inpaint=True)
                    target = imageFourCornersInpainting(target)
                    processed_frame = target
                    break
    if processed_frame is not None:
        print("COVER IMAGE FOUND!")
        cv2.imshow("image", processed_frame)
        cv2.waitKey(0)
    else:
        print("COVER NOT FOUND FOR %s" % videoLink)