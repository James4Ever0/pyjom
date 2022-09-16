# it contains subpixel motion vectors. fucking hell

source = ""
from mvextractor.videocap import VideoCap

while True:
    success, frame, motion_vectors, frame_type,timestamp = 