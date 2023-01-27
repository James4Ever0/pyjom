# check if is the video we want and extract data or discard.

# maybe you want some challange, so you can make one, right?

# videos = [
#     "286760784_part1-00001.mp4",
#     "329297394_part1-00001.mp4",
#     "541755429_part1-00001.mp4",
#     "842224692_part1-00001.mp4",
# ]

import os

# videos = [fpath for fpath in os.listdir(".") if fpath.endswith(".mp4")]
videos = ["480138800_part1.mp4"] # mine video, classic!

# we create dataset here.
# use some short cuts for progression.

frame_step = 10
import cv2
import progressbar

from pynput.keyboard import Listener

lastKey = ["not_c"]


def on_press(key):
    lastKey[0] = "not_c"
    try:
        # print("alphanumeric key {0} pressed".format(key.char))
        if key.char in ["c", "C"]:
            lastKey[0] = "c"
    except AttributeError:
        # print("special key {0} pressed".format(key))
        ...


def on_release(key):
    # print("{0} released".format(key))
    ...


listener = Listener(on_press=on_press, on_release=on_release)
listener.start()
# with listener:
#     listener.join()

# how do you arrange such data?

fields = ["filename", "frame_index", "x", "y", "w", "h"]
import csv

for index, video in enumerate(videos):
    with open(f'{video.split(".")[0]}.csv', "w+") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
        print("reading video:", index)
        roi = None
        cap = cv2.VideoCapture(video)
        for vindex in progressbar.progressbar(
            range(0, int(cap.get(cv2.CAP_PROP_FRAME_COUNT)), frame_step)
        ):
            cap.set(cv2.CAP_PROP_POS_FRAMES, vindex)
            succ, image = cap.read()
            if succ:
                roi_new = cv2.selectROI("roi", image)
                # key=cv2.waitKey(0)
                print("roi_new:", roi_new)
                print("last key:", lastKey[0])
                # print()
                # print('keycode:',key)
                if roi_new == (0, 0, 0, 0):
                    if lastKey[0] == "c":
                        # this is cancelled. roi will be nothing!
                        roi = None
                else:
                    roi = roi_new
                print("roi:", roi)
                for i in range(frame_step):
                    roi_index = vindex + i
                    data = [video, roi_index]
                    if roi == None:
                        data += [0, 0, 0, 0]
                    else:
                        data += list(roi)
                    csvwriter.writerow(data)
        cap.release()
