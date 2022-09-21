import ffmpeg

videoPath = "/root/Desktop/works/pyjom/samples/video/corrupt_video.gif"
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