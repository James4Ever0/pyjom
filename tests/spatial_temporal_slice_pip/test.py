target_video = "/media/root/help/pyjom/samples/video/LiGlReJ4i.mp4" # 娜姐驾到 卡成傻逼

# you should quit those which has unexpected long frame processing loops.

# mask the area which has text on it. fill the area and blur the boundary.

# you could also trash those videos with pip detected.

import cv2

# shit it has low speed... canny

cap = cv2.VideoCapture(target_video)

ret = 1

while True:
    ret, frame = cap.read()
    if ret is None: break
