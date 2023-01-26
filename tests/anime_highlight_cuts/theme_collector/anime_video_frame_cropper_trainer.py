# check if is the video we want and extract data or discard.

# maybe you want some challange, so you can make one, right?

videos = [
    "286760784_part1-00001.mp4",
    "329297394_part1-00001.mp4",
    "541755429_part1-00001.mp4",
    "842224692_part1-00001.mp4",
]

# we create dataset here. 
# use some short cuts for progression.

frame_step = 10
import cv2
import progressbar
for index, video in enumerate(videos):
    print("reading video:", index)
    cap = cv2.VideoCapture(video)
    for vindex in progressbar.progressbar(range(0, int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),frame_step)):
        cap.set(cv2.CAP_PROP_POS_FRAMES, vindex)
        succ, image = cap.read()
        if succ:
            roi_new= cv2.selectROI('roi',image)
            key=cv2.waitKey(0)
            print('roi:',roi_new)
            print()
            print('keycode:',key)
    cap.close()