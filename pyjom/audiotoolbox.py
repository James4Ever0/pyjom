# first and foremost is the audio correction, the volume detector, the audio detector.
# https://trac.ffmpeg.org/wiki/AudioVolume

# but first how to get the audio duration?
# for video we have caer. but for audio?

import audioread
from lazero.utils.logger import sprint
    import ffmpeg

def getAudioDuration(audioFilePath):
    with audioread.audio_open(audioFilePath) as f:
        totalSeconds = f.duration
    return totalSeconds
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