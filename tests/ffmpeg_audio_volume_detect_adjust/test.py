# ffmpeg -i video.avi -af "volumedetect"
# shall we get the output?
# we can also detect if the stream does not have audio stream.
import sys
import parse

pyjom_path = "/root/Desktop/works/pyjom"
sys.path.append(pyjom_path)
import ffmpeg
from pyjom.audiotoolbox import getAudioDuration
from pyjom.medialang.processors.dotProcessor.videoProcessor import executeEditlyScript
from lazero.utils.logger import sprint

# import os
# import json
# import subprocess

# def executeEditlyScript(medialangTmpDir, editly_json):
#     editlyJsonSavePath = os.path.join(medialangTmpDir, "editly.json")
#     with open(editlyJsonSavePath, "w+", encoding="utf8") as f:
#         f.write(json.dumps(editly_json, ensure_ascii=False))
#     print("EXECUTING EDITLY JSON AT %s" % editlyJsonSavePath)
#     commandline = ["xvfb-run", "editly", "--json", editlyJsonSavePath]
#     print(commandline)
#     status = subprocess.run(commandline)  # is it even successful?
#     returncode = status.returncode
#     assert returncode == 0
#     print("RENDER SUCCESSFUL")


def create_black_video_without_audio(duration, mediapath):
    # ffmpeg -f lavfi -i color=c=black:s=1280x720:r=5 -i audio.mp3 -crf 0 -c:a copy -shortest output.mp4
    # length is in seconds.
    videoInput = "color=c=black:s=1280x720:r=5"
    ffmpeg.input(videoInput, f="lavfi", t=duration).output(mediapath, crf=0).run(
        overwrite_output=True
    )


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
        print(stderr)
        print("error when detecting volume for: %s" % mediapath)
        error = True
    if debug:
        print("MEDIA PATH: %s" % mediapath)
        print("VOLUME:", volDict)
        sprint("ERROR STATUS:", error)
    return volDict, error


import subprocess


def adjustVolumeInMedia(
    mediaPath, outputPath, targets={"mean": -10.8, "max": 0.0}, overwrite_output=False, algorithm=[]
):  # must set target volume.

    # use ffmpeg-normalize?
    # use aac for mp4 output. let's do it!
    target_level = targets.get("mean", None)
    true_peak = targets.get("max", None)
    commandline = ["ffmpeg-normalize", "-o", outputPath, "-pr", '-nt',algorithm]
    # now much better. let's see if we have other methods.
    # VOLUME NORMALIZATION SUCCESSFUL
    # MEDIA PATH: normalized.mp4
    # VOLUME: {'mean': -11.0, 'max': 0.0}
    # ERROR STATUS: False
    # commandline = ["ffmpeg-normalize", "-o", outputPath, "-pr"]
    # VOLUME: {'mean': -13.2, 'max': 0.0}
    # the 'mean' is still not correctified.
    # ERROR STATUS: False
    if outputPath.lower().endswith(".mp4"):
        commandline += ["-c:a", "aac"]
    if target_level:
        commandline += ["-t", str(target_level)]
    if true_peak:
        commandline += ["-tp", str(true_peak)]
    if overwrite_output:
        commandline+= ['-f']
    commandline += [mediaPath]
    status = subprocess.run(commandline)  # is it even successful?
    returncode = status.returncode
    assert returncode == 0
    print("VOLUME NORMALIZATION SUCCESSFUL")
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
