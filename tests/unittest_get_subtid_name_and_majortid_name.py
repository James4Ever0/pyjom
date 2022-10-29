from bilibili_api import search
BSP = search.bilibiliSearchParams

for key,value in BSP.all.tids.__dict__.items():
    try:
        major_tid = value.tid
        print(key, value, major_tid)
    except:
        pass

