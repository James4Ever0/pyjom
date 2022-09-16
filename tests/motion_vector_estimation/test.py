# it contains subpixel motion vectors. fucking hell

source = ""
from mvextractor.videocap import VideoCap


cap = VideoCap()
cap.open(source)
while True:
    success, frame, motion_vectors, frame_type,timestamp = cap.read()