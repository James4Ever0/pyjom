from test_commons import *

from pyjom.platforms.bilibili.uploader import uploadVideo
import uuid

randomString = str(uuid.uuid4())
uploadVideo(description='test video',dynamic='nothing', tagString='狗狗',title='just a test {}'.format(randomString),videoPath=videoPath, cover_path=cover_path, ) # it is with credential right now.