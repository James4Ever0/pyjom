import av
source = "/root/Desktop/works/pyjom/samples/video/nearly_duplicate_frames_detection_30fps_blend.mp4"  # this is evil. it defeats my shit.

container = av.open(source)

counts = 0
for frame in container.decode(video=0):
    print("KEY FRAME?",frame.key_frame)