from test_commons import *
from pyjom.videotoolbox import getVideoFrameSampler

videoPath = "/root/Desktop/works/pyjom/samples/video/LkS8UkiLL.mp4"

imageSet = getVideoFrameSampler(videoPath, 0, 5, 60)
# print(imageSet)
# print(type(imageSet))
# # breakpoint()
