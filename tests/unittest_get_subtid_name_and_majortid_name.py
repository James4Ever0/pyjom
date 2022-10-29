from bilibili_api import search

BSP = search.bilibiliSearchParams

def getMajorMinorTidsMappings()
    majorMinorMappings = {}
    for key, value in BSP.all.tids.__dict__.items():
        try:
            major_tid = value.tid
            if debug:
                print("MAJOR", key, major_tid)
            content = {"major": {"tid": major_tid, "name": key}}
            majorMinorMappings.update({major_tid: content, key: content})
            for subkey, subvalue in value.__dict__.items():
                if subkey != "tid" and type(subvalue) == int:
                    if debug:
                        print("MINOR", subkey, subvalue)
                    content = {
                        "major": {"tid": major_tid, "name": key},
                        "minor": {"tid": subvalue, "name": subkey},
                    }
                    majorMinorMappings.update({subvalue: content, subkey: content})
        except:
            pass
    return majorMinorMappings
