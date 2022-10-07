# ffmpeg -i video.avi -af "volumedetect"
# shall we get the output?
# we can also detect if the stream does not have audio stream.
import sys
import parse

pyjom_path = "/root/Desktop/works/pyjom"
sys.path.append(pyjom_path)
import ffmpeg
from pyjom.audiotoolbox import getAudioDuration
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
    fast=True
    output_path = 'volDetect_test.mp4'
    videoFilePath = 'black_video_with_equal_length_of_audio.mp4'
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
    duration = cutTo = audio_duration
    cutFrom = 0
    mute=True
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
    clip['layers'].append(layer)
    editly_json['clips'].append(clip)
    # execute the thing.
    executeEditlyScript(".", editly_json)

def detect_volume_average(mediapath):
    # ffmpeg -i input.wav -filter:a volumedetect -f null /dev/null
    audio = ffmpeg.input(mediapath).audio
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
        print("error when detecting volume for: %s" % mediapath)
        error = True
    return volDict, error
