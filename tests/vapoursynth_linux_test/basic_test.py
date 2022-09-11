videoPath = "/root/Desktop/works/pyjom/samples/video/dog_with_text.mp4"
# videoPath = "/Users/jamesbrown/desktop/works/pyjom_remote/samples/video/dog_with_text.mp4"

from vapoursynth import core
video = core.ffms2.Source(source=videoPath)
video = core.std.Transpose(video)
video.set_output()

# vspipe is a wrapper around existing apis. vapoursynth can only generate raw frame data so we cannot encode video here alone. maybe we need opencv for this?
# opencv preview https://github.com/UniversalAl/view