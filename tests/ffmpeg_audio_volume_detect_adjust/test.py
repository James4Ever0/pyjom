# ffmpeg -i video.avi -af "volumedetect"
# shall we get the output?
# we can also detect if the stream does not have audio stream.
import sys
import parse

pyjom_path = "/root/Desktop/works/pyjom"
sys.path.append(pyjom_path)
# import ffmpeg
from pyjom.audiotoolbox import getAudioDuration
from pyjom.medialang.processors.dotProcessor.videoProcessor import executeEditlyScript

# import os
import json


# videotoolbox?
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


# commons.
from pyjom.commons import determineMediaTypeByExtension

# audiotoolbox.
from pyjom.audiotoolbox import detect_volume_average

import subprocess

from typing import Literal

# audiotoolbox
def adjustVolumeInMedia(
    mediaPath,
    outputPath,
    targets={
        "mean": -10.8,  # -13.2 fuck.
        "max": 0.0,
    },  # what is the real value anyway? we want the volume fetched from web.
    overwrite_output=False,
    bitrate=320000,
    algorithm: Literal["rms", "ebu", "peak"] = "rms",
):  # must set target volume.

    # use ffmpeg-normalize?
    # use aac for mp4 output. let's do it!
    target_level = targets.get("mean", None)
    true_peak = targets.get("max", None)
    commandline = [
        "ffmpeg-normalize",
        "-o",
        outputPath,
        "-pr",
        "-nt",
        algorithm,
    ]
    commandline += ["-b:a", str(bitrate)]  # the bitrate part.
    # now much better. let's see if we have other methods.
    # VOLUME NORMALIZATION SUCCESSFUL
    # MEDIA PATH: normalized.mp4
    # VOLUME: {'mean': -11.0, 'max': 0.0}
    # ERROR STATUS: False
    # commandline = ["ffmpeg-normalize", "-o", outputPath, "-pr"]
    # VOLUME: {'mean': -13.2, 'max': 0.0}
    # the 'mean' is still not correctified.
    # ERROR STATUS: False
    # video codec we use 'copy' if the extension name is the same.
    outputPathExtension = outputPath.lower().split(".")[-1]
    mediaPathExtension = mediaPath.lower().split(".")[-1]
    outputMediaType = determineMediaTypeByExtension(outputPathExtension)
    # treat this as a common repository.
    if outputPathExtension == mediaPathExtension and outputMediaType == "video":
        commandline += ["-c:v", "copy"]
    # problem is, the container must be video compabible.
    # list the thing here?
    if outputPathExtension == "mp4":
        commandline += ["-c:a", "aac"]
    if target_level:
        commandline += ["-t", str(target_level)]
    if true_peak:
        commandline += ["-tp", str(true_peak)]
    if overwrite_output:
        commandline += ["-f"]
    commandline += [mediaPath]
    status = subprocess.run(commandline)  # is it even successful?
    returncode = status.returncode
    try:
        assert returncode == 0
        print("VOLUME NORMALIZATION SUCCESSFUL")
    outputPath,
        return  
    # media = ffmpeg.input(videoPath)
    # audio = media.audio
    # video = media.video
    # audio = audio.filter()


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

# commons.
def getMediaBitrate(mediaPath, audioOnly=False, videoOnly=False):
    # demo output:
    # {'programs': [], 'streams': [{'bit_rate': '130770'}]}
    commandArguments = [
        "ffprobe",
        "-i",
        mediaPath,
        "-v",
        "quiet",
    ]
    if audioOnly:
        commandArguments += [
            "-select_streams",
            "a:0",
        ]
    elif videoOnly:
        commandArguments += [
            "-select_streams",
            "v:0",
        ]
    commandArguments += [
        "-show_entries",
        "stream=bit_rate",
        "-hide_banner",
        "-print_format",
        "json",
    ]
    result = subprocess.run(commandArguments, capture_output=True, encoding="UTF-8")
    stdout = result.stdout
    stderr = result.stderr
    try:
        assert result.returncode == 0
        stdout_json = json.loads(stdout)
        return stdout_json
    except:
        import traceback

        traceback.print_exc()
        print("potential error logs:")
        print(stderr)
        print("error when getting media bitrate")
        return {}


# videotoolbox.
# you also need to get the bitrate of video/audio
def getVideoBitrate(mediaPath):
    return int(getMediaBitrate(mediaPath, videoOnly=True)["streams"][0]["bitrate"])
    # you might want this magic.


# audiotoolbox.
def getAudioBitrate(mediaPath):
    return int(getMediaBitrate(mediaPath, audioOnly=True)["streams"][0]["bitrate"])
