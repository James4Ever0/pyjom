videoLink = "https://www.bilibili.com/video/BV1Cb4y1s7em"  # this is a dog.

# videoLink = "https://www.bilibili.com/video/BV1Lx411B7X6"  # multipart download

# from lazero.filesystem.temp import tmpfile

import yt_dlp

# import pyidm

path = "/dev/shm/testVideo.mp4"
from test_commons import *
from lazero.utils.importers import cv2_custom_build_init

cv2_custom_build_init()
import cv2

from pyjom.videotoolbox import getVideoFrameSampler
from pyjom.imagetoolbox import imageDogCatCoverCropAdvanced

# from pyjom.imagetoolbox import (
#     bezierPaddleHubResnet50ImageDogCatDetector,
#     # we deprecate this thing to make it somehow better.
#     getImageTextAreaRatio,
#     imageFourCornersInpainting,
#     imageCropoutBlackArea,
#     imageCropoutBlurArea,
#     imageDogCatDetectionForCoverExtraction,
#     imageLoader,
# )
from pyjom.commons import checkMinMaxDict


import os

# with tmpfile(path=path, replace=True) as TF:
if os.path.exists(path):
    os.remove(path)

x = yt_dlp.YoutubeDL(
    {
        "outtmpl": path,  # seems only video p1 is downloaded.
    }
)
y = x.download([videoLink])
# shall you use frame sampler instead of iterator? cause this is dumb.
# breakpoint()
from pyjom.videotoolbox import corruptVideoFilter

video_fine = corruptVideoFilter(path)

if not video_fine:
    print("VIDEO FILE CORRUPTED")
    exit()

from caer.video.frames_and_fps import get_duration


duration = get_duration(path)
mSampleSize = int(duration / 2)  # fps = 0.5 or something?
processed_frame = None
dog_or_cat = "dog"

for frame in getVideoFrameSampler(path, -1, -1, sample_size=mSampleSize, iterate=True):
    # animalCropDiagonalRect = imageDogCatDetectionForCoverExtraction(
    #     frame,
    #     dog_or_cat=dog_or_cat,
    #     confidence_threshold=confidence_threshold,
    #     crop=False,
    # )  # you must use gpu this time.
    # if animalCropDiagonalRect is not None:  # of course this is not None.
    # we need to identify this shit.
    # if checkMinMaxDict(text_area_ratio, text_area_threshold):
    processed_frame = imageDogCatCoverCropAdvanced(frame, dog_or_cat=dog_or_cat)
    if processed_frame is not None:
        # blurValue = imageCropoutBlurArea(processed_frame, value=True)
        # print("BLUR VALUE:", blurValue)
        # if not checkMinMaxDict(blurValue, blurValue_threshold):
        #     # will skip this one since it is not so clear.
        #     continue
        break
if processed_frame is not None:
    print("COVER IMAGE FOUND!")
    processed_frame_show = cv2.resize(processed_frame, (int(1920 / 2), int(1080 / 2)))
    cv2.imshow("image", processed_frame_show)
    cv2.waitKey(0)
else:
    print("COVER NOT FOUND FOR %s" % videoLink)
