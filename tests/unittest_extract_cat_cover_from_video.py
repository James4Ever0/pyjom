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
from pyjom.imagetoolbox import (
    # bezierPaddleHubResnet50ImageDogCatDetector,
    # we deprecate this thing to make it somehow better.
    getImageTextAreaRatio,
    imageFourCornersInpainting,
    imageCropoutBlackArea,
    imageCropoutBlurArea,
    imageDogCatDetectionForCoverExtraction
)
from pyjom.commons import checkMinMaxDict

dog_or_cat = "dog"
# confidence_threshold = {"min": 0.8}
confidence_threshold = 0.85
# confidence_threshold = {"min": 0.7}
text_area_threshold = {"max": 0.2}
# gpu = True

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
for frame in getVideoFrameSampler(path, -1, -1, sample_size=mSampleSize, iterate=True):
    text_area_ratio = getImageTextAreaRatio(frame)
    # text_area_ratio = getImageTextAreaRatio(frame, gpu=gpu)
    print("TEXT AREA RATIO", text_area_ratio)
    if checkMinMaxDict(text_area_ratio, text_area_threshold):
        mFrame = getImageTextAreaRatio(frame, inpaint=True)
        animalCropDiagonalRect = imageDogCatDetectionForCoverExtraction(mFrame, dog_or_cat=dog_or_cat,confidence_threshold=confidence_threshold, crop=False) # you must use gpu this time.
        if animalCropDiagonalRect is not None:
            mFrame = imageCropoutBlackArea(mFrame)
            mFrame = imageCropoutBlurArea(mFrame)
            mFrame = imageFourCornersInpainting(mFrame)
            processed_frame = imageDogCatDetectionForCoverExtraction(mFrame, dog_or_cat=dog_or_cat,confidence_threshold=confidence_threshold, crop=True)
            if processed_frame is not None:
                
        # detections = bezierPaddleHubResnet50ImageDogCatDetector(frame, use_gpu=gpu)
        # mDetections = [x for x in detections if x["identity"] == dog_or_cat]
        # mDetections.sort(key=lambda x: -x["confidence"])  # select the best one.
        # if len(mDetections) > 0:
        #     best_confidence = mDetections[0]["confidence"]
        #     print("BEST CONFIDENCE:", best_confidence)
        #     if checkMinMaxDict(best_confidence, confidence_threshold):
        #         target = getImageTextAreaRatio(frame, inpaint=True, gpu=gpu)
        #         target = imageFourCornersInpainting(target)
        #         processed_frame = target
        #         break
if processed_frame is not None:
    print("COVER IMAGE FOUND!")
    cv2.imshow("image", processed_frame)
    cv2.waitKey(0)
else:
    print("COVER NOT FOUND FOR %s" % videoLink)
