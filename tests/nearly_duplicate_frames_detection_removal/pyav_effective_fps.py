import av
source = "/root/Desktop/works/pyjom/samples/video/nearly_duplicate_frames_detection_30fps_blend.mp4"  # this is evil. it defeats my shit.

container = av.open(source)

for frame in container.decode(video=0):
    print(frame.key_frame)