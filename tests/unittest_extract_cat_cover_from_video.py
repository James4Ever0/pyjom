videoLink = "https://www.bilibili.com/video/BV1Cb4y1s7em"

from lazero.filesystem.temp import tmpfile

import yt_dlp
# import pyidm

path = "/dev/shm/randomName.mp4"
from test_commons import *
from pyjom.videotoolbox import getVideoFrameIteratorWithFPS
from pyjom.imagetoolbox import
with tmpfile(path=path) as TF:
    x = yt_dlp.YoutubeDL({"outtmpl":path,'format':'[ext=mp4]'})
    y = x.download([videoLink])
    for frame in getVideoFrameIteratorWithFPS(path, -1,-1,fps=0.5):
        