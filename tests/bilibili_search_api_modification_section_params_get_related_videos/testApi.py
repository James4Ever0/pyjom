from bilibili_api import sync, search

BSP = search.bilibiliSearchParams()

result = sync(
    search.search(
        keyword="汪汪",
        params={"tids": BSP.all.tids.动物圈.tid, "duration": BSP.all.duration._10分钟以下},
        page=1
    )
)
