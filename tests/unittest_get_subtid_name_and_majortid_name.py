from bilibili_api import search

BSP = search.bilibiliSearchParams

for elem in BSP.all.tids:
    print(elem)

