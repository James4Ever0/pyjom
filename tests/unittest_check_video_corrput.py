import ffmpeg

videoPath = "/root/Desktop/works/pyjom/samples/video/"
try:
    (
        ffmpeg
        .input(videoPath)
        .output("null", f="null")
        .run()
    )
except ffmpeg._run.Error:
    print("corrupt video")
else:
    print("video is fine")