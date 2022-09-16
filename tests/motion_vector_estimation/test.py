# it contains subpixel motion vectors. fucking hell

source = "/root/Desktop/works/pyjom/samples/video/dog_with_text.mp4"
from lazero.utils.importers import cv2_custom_build_init
cv2_custom_build_init()
from mvextractor.videocap import VideoCap


cap = VideoCap()
cap.open(source) # wtf is going on here?
# if there is nothing we will breakup
while True:
    success, frame, motion_vectors, frame_type,timestamp = cap.read()
    if success:
        print(motion_vectors)
        print(motion_vectors.shape)