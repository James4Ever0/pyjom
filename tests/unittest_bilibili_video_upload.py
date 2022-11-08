from test_commons import *

from pyjom.platforms.bilibili.uploader import uploadVideo
import uuid

randomString = str(uuid.uuid4())
import ffmpeg
# how about let's generate shit?
# use multithread uploader instead of that.
import tempfile
with tempfile.NamedTemporaryFile(suffix='.jpeg') as pic:
    cover_path = pic.name
    with tempfile.NamedTemporaryFile(suffix=".mp4") as f:
        videoPath = f.name
        ffmpeg.input("nullsrc=s=1280x720",f=-f lavfi)
        uploadVideo(
            description="test video",
            dynamic="nothing",
            tagString="狗狗",
            title="just a test {}".format(randomString),
            videoPath=videoPath,
            cover_path=cover_path,
            multithread=True,
        )  # it is with credential right now.
