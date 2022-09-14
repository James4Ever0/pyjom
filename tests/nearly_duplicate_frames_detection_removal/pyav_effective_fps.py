import av
# source = "/root/Desktop/works/pyjom/samples/video/nearly_duplicate_frames_detection_30fps_blend.mp4"  # this is evil. it defeats my shit.
# KEYFRAME PERCENT: 1.36 %

# source = "/root/Desktop/works/pyjom/samples/video/dog_with_text.mp4"  # this is evil. it defeats my shit.
# KEYFRAME PERCENT: 0.76 %
# wtf?
# even smaller.

source = "/root/Desktop/works/pyjom/samples/video/karaoke_effects_source.mp4"

container = av.open(source)

mList = []
for frame in container.decode(video=0):
    mList.append(frame.key_frame)

print("KEYFRAME PERCENT: {:.2f} %".format(100*sum(mList)/len(mList)), len(mList))