from bilibili_api import search

BSP = search.bilibiliSearchParams

majorMinorMappings = {}

for key, value in BSP.all.tids.__dict__.items():
    try:
        major_tid = value.tid
        # print("MAJOR", key, major_tid)
        majorMinorMappings.update(
            {major_tid: {"major": {"tid": major_tid, "name": key}}}
        )
        majorMinorMappings.update({key: {"major": {"tid": major_tid, "name": key}}})
        for subkey, subvalue in value.__dict__.items():
            if subkey != "tid" and type(subvalue) == int:
                print("MINOR", subkey, subvalue)
                majorMinorMappings.update(
                    {
                        subvalue: {
                            "major": {"tid": major_tid, "name": key},
                            "minor": {"tid": subvalue, "name": subkey},
                        }
                    }
                )
                majorMinorMappings.update(
                    {
                        subkey: {
                            "major": {"tid": major_tid, "name": key},
                            "minor": {"tid": subvalue, "name": subkey},
                        }
                    }
                )
    except:
        pass
