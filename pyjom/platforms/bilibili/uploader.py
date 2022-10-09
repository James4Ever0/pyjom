from bilibili_api import video_uploader, Credential
from pyjom.platforms.bilibili.credentials import getCredentialByDedeUserId
# you may use the 'sync' method elsewhere.
async def uploadVideo(
    # sessdata="",
    # bili_jct="",
    # buvid3="", # credentials.
    dedeuserid:str="397424026",
    description:str="",
    dynamic:str="",
    tagString:str="",
    tagId:int=21, # what is 21? -> 日常
    title="",
    close_danmaku=False,
    close_reply=False,
    videoPath="",
    cover_path="",
    # threads=3,
):
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
        path = videoPath,
        title=title,
        description=description,
    )  # are you sure?
    uploader = video_uploader.VideoUploader(
        [page], meta, credential,cover_path=cover_path
    )

    # will this work as expected?
    @uploader.on("__ALL__")
    async def ev(data):
        print(data)

    await uploader.start()