from test_commons import *
import os
from pyjom.platforms.bilibili.uploader import uploadVideo
import uuid

randomString = str(uuid.uuid4())
# import ffmpeg
# how about let's generate shit?
# use multithread uploader instead of that.
import tempfile

# import random
duration = 5
with tempfile.NamedTemporaryFile(suffix=".jpeg") as pic:
    cover_path = pic.name
    with tempfile.NamedTemporaryFile(suffix=".mp4") as f:
        videoPath = f.name
        command = f"""ffmpeg -y -f lavfi -i nullsrc=s=1920x1080 -filter_complex "geq=random(1)*255:128:128;aevalsrc=-2+random(0)" -t {duration:.2f} {videoPath}"""
        os.system(command)
        picgen_command = f"""ffmpeg -y -i {videoPath} -ss 1 {cover_path}"""
        os.system(picgen_command)
        print("uploading video")
        reply = uploadVideo(
            description="test video",
            dynamic="nothing",
            tagString="狗狗",
            title="just a test {}".format(randomString),
            videoPath=videoPath,
            cover_path=cover_path,
            multithread=True,
        )  # it is with credential right now.
        print("reply:", reply)  # reply true? what the fuck?
        print("----")
        breakpoint()
