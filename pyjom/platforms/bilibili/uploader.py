from bilibili_api import sync, video_uploader, Credential

async def main(sessdata="", bili_jct="", buvid3=""):
    credential = Credential(sessdata=sessdata, bili_jct=bili_jct, buvid3=buvid3)
    # 具体请查阅相关文档
    meta = {
            "copyright": 1, 
            "source": "", # no source?
            "desc": desc,
            "desc_format_id": 0,
            "dynamic": dynamic, # could be the same as desc.
            "interactive": 0,
            "open_elec": 1,
            "no_reprint": 1,
            "subtitles": {
                "lan": "",
                "open": 0
            },
            "tag": tagString,
            "tid": tagId, # original is 21. what is it?
            "title": title,
            "up_close_danmaku": close_danmaku,
            "up_close_reply": close_reply
        }
    page = video_uploader.VideoUploaderPage(video_stream=open(videoPath, 'rb'), title=title, description='', extension=videoExtension)
    uploader = video_uploader.VideoUploader([page], meta, credential, threads=1)

    @uploader.on("__ALL__")
    async def ev(data):
        print(data)

    await uploader.start()


sync(main())