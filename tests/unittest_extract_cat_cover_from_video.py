videoLink = "https://www.bilibili.com/video/BV1Cb4y1s7em"

from lazero.filesystem.temp import tmpfile

import yt_dlp
# import pyidm

path = "/dev/shm/testVideo.mp4"
from test_commons import *
from pyjom.videotoolbox import getVideoFrameIteratorWithFPS
from pyjom.imagetoolbox import bezierPaddleHubResnet50ImageDogCatDetector

dog_or_cat = "dog"

with tmpfile(path=path) as TF:
    x = yt_dlp.YoutubeDL({"outtmpl":path,'format':'[ext=mp4]'})
    y = x.download([videoLink])
    for frame in getVideoFrameIteratorWithFPS(path, -1,-1,fps=0.5):
        detections = bezierPaddleHubResnet50ImageDogCatDetector(frame)
        mDetections = [x for x in detections if x['identity'] == dog_or_cat]
        mDetections.sort(key=lambda x: -x['confidence'])