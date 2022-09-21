import ffmpeg

try:
    (
        ffmpeg
        .input("corrupt_video.mp4")
        .output("null", f="null")
        .run()
    )
except ffmpeg._run.Error:
    print("corrupt video")
else:
    print("video is fine")