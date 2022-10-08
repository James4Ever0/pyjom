from bilibili_api import sync, video_uploader, Credential

async def main(sessdata="", bili_jct="", buvid3=""):
    credential = Credential(sessdata=sessdata, bili_jct=bili_jct, buvid3=buvid3)
    # 具体请查阅相关文档
    meta = {
            "copyright": 1,
            "source": "",
            "desc": "desc",
            "desc_format_id": 0,
            "dynamic": dynamic, # 
            "interactive": 0,
            "open_elec": 1,
            "no_reprint": 1,
            "subtitles": {
                "lan": "",
                "open": 0
            },
            "tag": "标签1,标签2,标签3",
            "tid": 21,
            "title": "title",
            "up_close_danmaku": True,
            "up_close_reply": True
        }
    page = video_uploader.VideoUploaderPage(video_stream=open('video.mp4', 'rb'), title='test', description='', extension='mp4')
    uploader = video_uploader.VideoUploader([page], meta, credential, threads=1)

    @uploader.on("__ALL__")
    async def ev(data):
        print(data)

    await uploader.start()


sync(main())