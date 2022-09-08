# motion detectors are used to track objects. though you may want to separate objects with it.
import numpy as np
import cv2
import pybgs as bgs
import talib  # wait till all points are stablized. find a way to stream this.

# suspect by static image analysis, and then create bounding box over the thing.
# check image quality.

# this can generate frame borders.

algorithm = (
    bgs.FrameDifference()
)  # this is not stable since we have more boundaries. shall we group things?
video_file = (
    "../../samples/video/dog_with_text.mp4"  # this is doggy video without borders.
)
# video_file = "../../samples/video/LiEIfnsvn.mp4" # this one with cropped boundaries.

capture = cv2.VideoCapture(video_file)
while not capture.isOpened():
    capture = cv2.VideoCapture(video_file)
    # cv2.waitKey(1000)
    # print("Wait for the header")

pos_frame = capture.get(1)

def getAppendArray(mx1, min_x, past_frames=19):
    return np.append(mx1[-past_frames:], min_x)


def getFrameAppend(frameArray, pointArray, past_frames=19):
    mx1, mx2, my1, my2 = [
        getAppendArray(a, b, past_frames=past_frames)
        for a, b in zip(frameArray, pointArray)
    ]
    return mx1, mx2, my1, my2


def getStreamAvg(a, timeperiod=10):  # to maintain stability.
    return talib.stream.EMA(a, timeperiod=timeperiod)


def checkChange(frame_x1, val_x1, h, change_threshold=0.2):
    return (abs(frame_x1 - val_x1) / h) > change_threshold  # really changed.


mx1, mx2, my1, my2 = [np.array([]) for _ in range(4)]
past_frames = 19
perc = 0.03
frame_num = 0
# what is the time to update the frame?

frame_x1, frame_y1, frame_x2, frame_y2 = [None for _ in range(4)]
reputation = 0
max_reputation = 3
minVariance = 10

frameDict = {}  # include index, start, end, coords.

frameIndex = 0
while True:
    flag, frame = capture.read()
    frameIndex += 1
    if flag:
        pos_frame = capture.get(1)  # this is getting previous frame without read again.
        img_output = algorithm.apply(frame)
        img_bgmodel = algorithm.getBackgroundModel()
        _, contours = cv2.findContours(
            img_output, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
        )
        # maybe you should merge all active areas.
        if contours is not None:
            # continue
            counted = False
            for contour in contours:
                [x, y, w, h] = cv2.boundingRect(img_output)
                if not counted:
                    min_x, min_y = x, y
                    max_x, max_y = x + w, y + h
                    counted = True
                else:
                    min_x = min(min_x, x)
                    min_y = min(min_y, y)
                    max_x = max(max_x, x + w)
                    max_y = max(max_y, y + h)
                    # only create one single bounding box.
            # print("points:",min_x, min_y, max_x,max_y)
            this_w = max_x - min_x
            this_h = max_y - min_y
            thresh_x = max(minVariance, int(perc * (this_w)))
            thresh_y = max(minVariance, int(perc * (this_h)))
            mx1, mx2, my1, my2 = getFrameAppend(
                (mx1, mx2, my1, my2), (min_x, max_x, min_y, max_y)
            )
            val_x1, val_x2, val_y1, val_y2 = [
                getStreamAvg(a) for a in (mx1, mx2, my1, my2)
            ]
            # not a number. float
            # will return False on any comparison, including equality.
            if (
                abs(val_x1 - min_x) < thresh_x
                and abs(val_x2 - max_x) < thresh_x
                and abs(val_y1 - min_y) < thresh_y
                and abs(val_y2 - max_y) < thresh_y
            ):
                needChange = False
                # this will create bounding rect.
                # this cannot handle multiple active rects.
                reputation = max_reputation
                if frame_x1 == None:
                    needChange = True
                elif (
                    checkChange(frame_x1, val_x1, this_w)
                    or checkChange(frame_x2, val_x2, this_w)
                    or checkChange(frame_y1, val_y1, this_h)
                    or checkChange(frame_y2, val_y2, this_h)
                ):
                    needChange = True
                    # the #2 must be of this reason.
                if needChange:
                    frame_x1, frame_y1, frame_x2, frame_y2 = [
                        int(a) for a in (min_x, min_y, max_x, max_y)
                    ]
                    print()
                    print("########FRAME CHANGED########")
                    frame_num += 1
                    frame_area = (frame_x2 - frame_x1) * (frame_y2 - frame_y1)
                    # update the shit.
                    coords = ((frame_x1, frame_y1), (frame_x2, frame_y2))
                    frameDict[frame_num] = {
                        "coords": coords,
                        "start": frameIndex,
                        "end": frameIndex,
                    }
                    print(
                        "FRAME INDEX: {}".format(frame_num)
                    )  # this is the indexable frame. not uuid.
                    print("FRAME AREA: {}".format(frame_area))
                    print("FRAME COORDS: {}".format(str(coords)))
                # allow us to introduce our new frame determinism.
            else:
                if reputation > 0:
                    reputation -= 1
            if frame_x1 is not None and reputation > 0:
                # you may choose to keep cutting the frame? with delay though.
                cv2.rectangle(
                    frame, (frame_x1, frame_y1), (frame_x2, frame_y2), (255, 0, 0), 2
                )
                frameDict[frame_num]["end"] = frameIndex
                # we mark the first and last time to display this frame.
            # how to stablize this shit?
        cv2.imshow("video", frame)
        # just video.
        # cv2.imshow('img_output', img_output)
        # cv2.imshow('img_bgmodel', img_bgmodel)

    else:
        cv2.waitKey(1000)
        break

    if 0xFF & cv2.waitKey(10) == 27:
        break


cv2.destroyAllWindows()
print("FINAL FRAME DETECTIONS:")
print(frameDict)
# {1: {'coords': ((80, 199), (496, 825)), 'start': 13, 'end': 269}, 2: {'coords': ((80, 381), (483, 644)), 'start': 297, 'end': 601}}
