from caer.video.frames_and_fps import get_res

videoPath = "/root/Desktop/works/pyjom/samples/video/cat_invalid_eye_rolling.gif"

width, height = get_res(videoPath)
print(width, height)
