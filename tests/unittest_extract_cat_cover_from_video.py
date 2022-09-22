videoLink = "https://www.bilibili.com/video/BV1Cb4y1s7em"

from lazero.filesystem.temp import tmpfile

import yt_dlp
# import pyidm

path = "/dev/shm/testVideo.mp4"
from test_commons import *
from pyjom.videotoolbox import getVideoFrameSampler
from pyjom.imagetoolbox import bezierPaddleHubResnet50ImageDogCatDetector
from pyjom.commons import checkMinMaxDict

dog_or_cat = "dog"
confidence_threshold = {"min":0.7}

with tmpfile(path=path) as TF:
    x = yt_dlp.YoutubeDL({"outtmpl":path,'format':'[ext=mp4]'})
    y = x.download([videoLink])
# shall you use frame sampler instead of iterator? cause this is dumb.
    from caer.video.frames_and_fps import get_duration
    duration = get_duration(path)
    mSampleSize = int(duration/2) # fps = 0.5 or something?
    for frame in getVideoFrameSampler(path, -1,-1,sample_size=mSampleSize,iterate=True):
        
        detections = bezierPaddleHubResnet50ImageDogCatDetector(frame)
        mDetections = [x for x in detections if x['identity'] == dog_or_cat]
        mDetections.sort(key=lambda x: -x['confidence']) # select the best one.
        if len(mDetections)>0:
            best_confidence = mDetections[0]['confidence']
            if checkMinMaxDict(best_confidence, confidence_threshold):
