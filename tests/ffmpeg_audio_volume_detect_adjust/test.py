# ffmpeg -i video.avi -af "volumedetect"
# shall we get the output?
# we can also detect if the stream does not have audio stream.
import ffmpeg


def create_black_video_without_audio(length, mediapath):
    # ffmpeg -f lavfi -i color=c=black:s=1280x720:r=5 -i audio.mp3 -crf 0 -c:a copy -shortest output.mp4
    # length is in seconds.
    videoInput = "color=c=black:s=1280x720:r=5"
    ffmpeg.input(videoInput, f="lavfi", t=length).output(mediapath, crf=0).run()


def create_test_video_with_editly(audio):  # length is calculated by the audio length.
    ...


def detect_volume_average(mediapath):
    ...
