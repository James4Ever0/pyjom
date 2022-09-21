from bilibili_api import sync, search

BSP = search.bilibiliSearchParams()

sync(search.search(keyword="汪汪",params = {}))