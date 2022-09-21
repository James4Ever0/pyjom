import ffmpeg

not_nice = ["invalid", "failed", "error"]
videoPath = "/root/Desktop/works/pyjom/samples/video/dog_with_large_text.gif"
# videoPath = "/root/Desktop/works/pyjom/samples/video/cute_cat_gif.gif"
# videoPath = "/root/Desktop/works/pyjom/samples/video/corrupt_video.gif"
corrupted = False
try:
    stdout, stderr = (
        ffmpeg.input(videoPath)
        .output("null", f="null")
        .run(capture_stdout=True, capture_stderr=True)
    )
    stderr_lower = stderr.decode("utf-8").lower()
    for word in not_nice:
        if word in stderr_lower:
            print("video is corrupted")
            corrupted = True
            break
except:
    import traceback

    traceback.print_exc()
    corrupted = True
    print("corrupt video")

if not corrupted:
    print("video is fine")
