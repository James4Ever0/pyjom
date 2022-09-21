import ffmpeg
"invalid","failed",'error']
videoPath = "/root/Desktop/works/pyjom/samples/video/corrupt_video.gif"
try:
    stdout, stderr = ffmpeg
        .input(videoPath)
        .output("null", f="null")
        .run(capture_stdout=True,capture_stderr=True
except ffmpeg._run.Error:
    print("corrupt video")
else:
    print("video is fine")