# it contains subpixel motion vectors. fucking hell

source = "/root/Desktop/works/pyjom/samples/video/dog_with_text.mp4"
from lazero.utils.importers import cv2_custom_build_init

cv2_custom_build_init()
from mvextractor.videocap import VideoCap


cap = VideoCap()
cap.open(source)  # wtf is going on here?
# if there is nothing we will breakup
while True:
    success, frame, motion_vectors, frame_type, timestamp = cap.read()
    if success:
        # what is the content of this motion vector?
        # print(motion_vectors)
        for mv in motion_vectors:
            (
                source_index,
                _,
                _,
                src_x,
                src_y,
                dst_x,
                dst_y,
                motion_x,
                motion_y,
                motion_scale,
            ) = mv.tolist()
            a
            # print('source',src_x, src_y)
            # print('destionation',dst_x, dst_y)
            # print('motion',motion_x, motion_y)
            # print("scale",motion_scale)

        # print(motion_vectors.shape)
    else:
        break
