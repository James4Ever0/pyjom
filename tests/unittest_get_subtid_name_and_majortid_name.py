from bilibili_api import search
BSP = search.bilibiliSearchParams

for key,value in BSP.all.tids.__dict__.items():
    try:
        major_tid = value.tid
        print("MAJOR",key, major_tid)
        for subkey, subvalue in value.__dict__.items():
            minor_tid = 
    except:
        pass

