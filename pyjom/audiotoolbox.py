# first and foremost is the audio correction, the volume detector, the audio detector.
# https://trac.ffmpeg.org/wiki/AudioVolume

# but first how to get the audio duration?
# for video we have caer. but for audio?

import audioread
from lazero.utils.logger import sprint
import ffmpeg
from typing import Literal
from pyjom.commons import *
import parse


def getAudioBitrate(mediaPath):
    return int(getMediaBitrate(mediaPath, audioOnly=True)["streams"][0]["bit_rate"])


def getAudioDuration(audioFilePath):
    with audioread.audio_open(audioFilePath) as f:
        totalSeconds = f.duration
    return totalSeconds  # is this float number or integer?
    # how about let's test this?


def detect_volume_average(mediapath, debug=False):
    # ffmpeg -i input.wav -filter:a volumedetect -f null /dev/null
    # audio = ffmpeg.input(mediapath)
    audio = ffmpeg.input(mediapath).audio
    # does not have audio track, so error occurs.
    # don't know how to capture the track. anyway, do put the audio into the test video.
    # might have exception. what to do with it then??
    volDict = {}
    error = False
    try:
        stdout, stderr = (
            audio.filter("volumedetect")
            .output("/dev/null", f="null")
            .run(capture_stdout=True, capture_stderr=True)
        )
        # where is the output?
        stderr = stderr.decode("utf-8")
        stderr_lines = stderr.split("\n")
        formatString = "[Parsed_volumedetect{}] {volumeType}_volume: {value:g} dB"
        for line in stderr_lines:
            line = line.strip()
            result = parse.parse(formatString, line)
            if result is not None:
                volumeType, value = result["volumeType"], result["value"]
                volDict.update({volumeType: value})
    except:
        import traceback

        traceback.print_exc()
        # print(stderr)
        # nothing will be shown in stderr, if there is no audio in the media container.
        print("error when detecting volume for: %s" % mediapath)
        error = True
    if debug:
        print("MEDIA PATH: %s" % mediapath)
        print("VOLUME:", volDict)
        sprint("ERROR STATUS:", error)
    return volDict, error


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
        return outputPath
    except:
        import traceback

        traceback.print_exc()
        print("error when normalizing audio for media: %s" % mediaPath)
    # media = ffmpeg.input(videoPath)
    # audio = media.audio
    # video = media.video
    # audio = audio.filter()
