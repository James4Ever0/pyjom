import ffmpeg
not_nice ["invalid","failed",'error']
videoPath = "/root/Desktop/works/pyjom/samples/video/corrupt_video.gif"
try:
    stdout, stderr = ffmpeg
        .input(videoPath)
        .output("null", f="null")
        .run(capture_stdout=True,capture_stderr=True
    stderr_lower = stder.decode('utf-8').lower()
    for word in not_nice:
        if word in stderr_lower:
            print("video is corrupted")
            corrupted=True
            break
    print("video is fine")
except:
    import traceback
    traceback.print_exc()
    print("corrupt video")


