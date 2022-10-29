from bilibili_api import search
BSP = search.bilibiliSearchParams

for key,value in BSP.all.tids.__dict__.items():
    if type(value) == object:
        print(key, value)

