# motion detectors are used to track objects. though you may want to separate objects with it.
import progressbar
import json
import pybgs as bgs
import numpy as np

import pathlib
import sys

site_path = pathlib.Path("/usr/local/lib/python3.9/site-packages")
cv2_libs_dir = site_path / 'cv2' / \
    f'python-{sys.version_info.major}.{sys.version_info.minor}'
print(cv2_libs_dir)
cv2_libs = sorted(cv2_libs_dir.glob("*.so"))
if len(cv2_libs) == 1:
    print("INSERTING:", cv2_libs[0].parent)
    sys.path.insert(1, str(cv2_libs[0].parent))

import cv2

# suspect by static image analysis, and then create bounding box over the thing.
# check image quality.

# for donga, you must change the framerate to skip identical frames.

# also donga have strange things you may dislike, e.g.: when only part of the image changes.

# algorithm = bgs.FrameDifference() # this is not stable since we have more boundaries. shall we group things?
# can we use something else?
algorithm = bgs.WeightedMovingVariance()
# this one with cropped boundaries.
# average shit.
# video_file = "../../samples/video/LiEIfnsvn.mp4"
# select our 娜姐驾到
video_file = "../../samples/video/LiGlReJ4i.mp4"
# video_file = "../../samples/video/LiEIfnsvn.mp4"

# denoising, moving average, sampler and  similar merge.
# moving average span: -20 frame to +20 frame

# denoising: 选区间之内相似的最多的那种

capture = cv2.VideoCapture(video_file)
while not capture.isOpened():
    capture = cv2.VideoCapture(video_file)
    cv2.waitKey(1000)
    print("Wait for the header")

defaultWidth = capture.get(cv2.CAP_PROP_FRAME_WIDTH)
defaultHeight = capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
total_frames = capture.get(cv2.CAP_PROP_FRAME_COUNT)
total_frames = int(total_frames)
pipFrames = []

defaultRect = [(0,0),(defaultWidth,defaultHeight)]

pos_frame = capture.get(1)

areaThreshold = int(0.2*0.2*defaultWidth*defaultHeight)

for index in progressbar.progressbar(range(total_frames)):
    # if index % 20 != 0: continue
    flag, frame = capture.read()
    if flag:
        pos_frame = capture.get(1)
        img_output = algorithm.apply(frame)
        imgThresh = img_output
        # imgMorph = cv2.GaussianBlur(img_output, (3,3), 0)
        # _,imgThresh = cv2.threshold(imgMorph, 1, 255, cv2.THRESH_BINARY)
        # img_bgmodel = algorithm.getBackgroundModel()
        # _, contours = cv2.findContours(
        #     imgThresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # maybe you should merge all active areas.
        # if contours is not None:
            # continue
            # counted = False
            # maxArea = 0
            # for contour in contours:
        [x, y, w, h] = cv2.boundingRect(img_output) # wtf is this?
        area = w*h
        if area > areaThreshold:
                # #     maxArea = area
                # if counted==False:
            min_x, min_y = x, y
            max_x, max_y = x+w, y+h
                # else:
                #     if x<min_x: min_x = x
                #     if x+w>max_x: max_x = x+w
                #     if y<min_y: min_y = y
                #     if y+w>max_y: max_y = y+w
            currentRect = [(min_x, min_y), (max_x, max_y)]
            pipFrames.append(currentRect.copy())
            defaultRect = currentRect.copy()
        else:
            pipFrames.append(defaultRect.copy())
            # how to stablize this shit?
        # cv2.imshow('video', frame)
        # cv2.imshow('img_output', img_output)
        # cv2.imshow('img_bgmodel', img_bgmodel)
        # cv2.imshow('imgThresh', imgThresh)
        # cv2.waitKey(100)


    else:
        # cv2.waitKey(1000)
        break

cv2.destroyAllWindows()


# we process this shit elsewhere.

with open("pip_meanVarianceSisterNa.json", 'w') as f:
    f.write(json.dumps(
        {"data": pipFrames, "width": defaultWidth, "height": defaultHeight}))
print("DATA DUMPED")
