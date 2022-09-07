videoPath = "/root/Desktop/works/pyjom/samples/video/dog_with_text.mp4"
# videoPath = "/Users/jamesbrown/desktop/works/pyjom_remote/samples/video/dog_with_text.mp4"

# reference: http://www.vapoursynth.com/doc/pythonreference.html

# The VideoFrame and AudioFrame classes contains one picture/audio chunk and all the metadata associated with it. It is possible to access the raw data using either get_read_ptr(plane) or get_write_ptr(plane) and get_stride(plane) with ctypes.

# A more Python friendly wrapping is also available where each plane/channel can be accessed as a Python array using frame[plane/channel].

# To get a frame simply call get_frame(n) on a clip. Should you desire to get all frames in a clip, use this code:

# for frame in clip.frames():
#     # Do stuff with your frame
#     pass



from vapoursynth import core
video = core.ffms2.Source(source=videoPath)
# video = core.std.Transpose(video)
# video.set_output()
# from viewKali import Preview
# clip = vs.core.lsmas.LibavSMASHSource('source.mp4')
# seems not working

# Preview(video)
# vspipe is a wrapper around existing apis. vapoursynth can only generate raw frame data so we cannot encode video here alone. maybe we need opencv for this?
# opencv preview https://github.com/UniversalAl/view