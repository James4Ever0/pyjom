from bilibili_api import search
BSP = search.bilibiliSearchParams

majorMinorMappings = {}

for key,value in BSP.all.tids.__dict__.items():
    try:
        major_tid = value.tid
        print("MAJOR",key, major_tid)
        for subkey, subvalue in value.__dict__.items():
            if subkey !='tid' and type(subvalue) == int:
                print("MINOR",subkey, subvalue)
                majorMinorMappings.append({subvalue:{'major':{'tid':}}})
    except:
        pass

