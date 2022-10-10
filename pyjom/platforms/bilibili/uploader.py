from bilibili_api import video_uploader
from pyjom.platforms.bilibili.credentials import getCredentialByDedeUserId
import os
from pyjom.platforms.bilibili.utils import bilibiliSync

# you may use the 'sync' method elsewhere.
# damn. ou
@bilibiliSync
async def uploadVideo(
    # sessdata="",
    # bili_jct="",
    # buvid3="", # credentials.
    dedeuserid: str = "397424026",
    description: str = "",
    dynamic: str = "",
    tagString: str = "",
    tagId: int = 21,  # what is 21? -> 日常
    title: str = "",
    close_danmaku: bool = False,
    close_reply: bool = False,
    videoPath: str = "",
    cover_path: str = "",
    # threads=3,
):
    assert os.path.exists(videoPath)
    assert os.path.exists(cover_path)
    credential = getCredentialByDedeUserId(dedeuserid)
    # videoExtension = videoPath.split(".")[-1].lower()
    # credential = Credential(sessdata=sessdata, bili_jct=bili_jct, buvid3=buvid3)
    # you can pass it from somewhere else.
    # 具体请查阅相关文档
    meta = {
        "copyright": 1,
        "source": "",  # no source?
        "desc": description,
        "desc_format_id": 0,
        "dynamic": dynamic,  # could be the same as desc.
        "interactive": 0,
        "open_elec": 1,
        "no_reprint": 1,
        "subtitles": {"lan": "", "open": 0},
        "tag": tagString,
        "tid": tagId,  # original is 21. what is it?
        "title": title,
        "up_close_danmaku": close_danmaku,
        "up_close_reply": close_reply,
    }
    page = video_uploader.VideoUploaderPage(
        path=videoPath,
        title=title,
        description=description,
    )  # are you sure?
    uploader = video_uploader.VideoUploader(
        [page], meta, credential, cover_path=cover_path
    )

    # will this work as expected?
    # @uploader.on("__ALL__")
    # async def ev(data):
    #     print(data)

    result = await uploader.start() # with bvid, aid as key.
    # please tell me where the fuck you upload my video upto?
    print('upload video result:', result)
    breakpoint() # comment it out later? or we will check why this upload fails. maybe it is because we have duplicated name/cover.
    return result['bvid'] # choose to be in this way?