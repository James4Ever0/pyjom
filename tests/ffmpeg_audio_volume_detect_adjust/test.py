# ffmpeg -i video.avi -af "volumedetect"
# shall we get the output?
# we can also detect if the stream does not have audio stream.
import sys

pyjom_path = "/root/Desktop/works/pyjom"
sys.path.append(pyjom_path)
from pyjom.audiotoolbox import getAudioDuration
from pyjom.medialang.processors.dotProcessor.videoProcessor import executeEditlyScript
from pyjom.videotoolbox import createPureColorVideo

# for test only.
def create_black_video_without_audio(duration, mediapath):
    createPureColorVideo(duration, mediapath)

# this is for test only. not for work.
# another editly script for another video. please?
def create_test_video_with_editly(audio):  # length is calculated by the audio length.
    audio_duration = getAudioDuration(audio)
    fast = True
    output_path = "volDetect_test.mp4"
    videoFilePath = "black_video_with_equal_length_of_audio.mp4"
    create_black_video_without_audio(audio_duration, videoFilePath)
    editly_json = {
        "width": 1920,
        "height": 1080,
        "fast": fast,
        "fps": 60,
        "outPath": output_path,
        "defaults": {"transition": None},
        "clips": [],
    }
    editly_json.update({"audioFilePath": audio})
    duration = cutTo = audio_duration
    cutFrom = 0
    mute = True
    clip = {
        "duration": duration,
        "layers": [],
    }
    layer = {
        "type": "video",
        "path": videoFilePath,
        "resizeMode": "contain",
        "cutFrom": cutFrom,
        "cutTo": cutTo,
        # that's how we mute it.
        "mixVolume": 1 - int(mute),
    }
    clip["layers"].append(layer)
    editly_json["clips"].append(clip)
    # execute the thing.
    executeEditlyScript(".", editly_json)
    print("media saved to: %s" % output_path)
    return output_path

from pyjom.audiotoolbox import detect_volume_average


if __name__ == "__main__":
    # perform our test.
    # are you sure this won't change the volume?
    audiopath = "/root/Desktop/works/pyjom/tests/music_analysis/exciting_bgm.mp3"
    detect_volume_average(audiopath, debug=True)
    # MEDIA PATH: /root/Desktop/works/pyjom/tests/music_analysis/exciting_bgm.mp3
    # VOLUME: {'mean': -10.8, 'max': 0.0}
    # ERROR STATUS: False
    # ______________________________
    output_path = create_test_video_with_editly(audiopath)
    detect_volume_average(output_path, debug=True)
    # volume changed!
    # MEDIA PATH: volDetect_test.mp4
    # VOLUME: {'mean': -16.8, 'max': -2.0}
    # ERROR STATUS: False
    # how to adjust the volume accordingly?
