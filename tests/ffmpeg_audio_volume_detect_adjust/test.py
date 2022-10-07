# ffmpeg -i video.avi -af "volumedetect"
# shall we get the output?
# we can also detect if the stream does not have audio stream.
import sys

pyjom_path = "/root/Desktop/works/pyjom"
sys.path.append(pyjom_path)
import ffmpeg
from pyjom.audiotoolbox import getAudioDuration


def create_black_video_without_audio(duration, mediapath):
    # ffmpeg -f lavfi -i color=c=black:s=1280x720:r=5 -i audio.mp3 -crf 0 -c:a copy -shortest output.mp4
    # length is in seconds.
    videoInput = "color=c=black:s=1280x720:r=5"
    ffmpeg.input(videoInput, f="lavfi", t=duration).output(mediapath, crf=0).run(
        overwrite_output=True
    )


def create_test_video_with_editly(audio):  # length is calculated by the audio length.
    audio_duration = getAudioDuration(audio)


def detect_volume_average(mediapath):
    # ffmpeg -i input.wav -filter:a volumedetect -f null /dev/null
    audio = ffmpeg.input(mediapath).audio
    stdout, stderr = audio.filter("volumedetect").output("/dev/null", f="null").run(capture_stdout=True, capture_stderr=True)