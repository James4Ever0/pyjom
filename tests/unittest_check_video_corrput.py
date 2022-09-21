import ffmpeg
not_nice ["invalid","failed",'error']
videoPath = "/root/Desktop/works/pyjom/samples/video/corrupt_video.gif"
try:
    stdout, stderr = ffmpeg
        .input(videoPath)
        .output("null", f="null")
        .run(capture_stdout=True,capture_stderr=True
    stderr_lower = stder.decode
    for word in not_nice:
        if word in
    print("video is fine")
except ffmpeg._run.Error:
    print("corrupt video")


