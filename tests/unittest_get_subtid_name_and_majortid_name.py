from bilibili_api import search

BSP = search.bilibiliSearchParams


def getMajorMinorTopicMappings(debug: bool = False):
    majorMinorMappings = {}
    for key, value in BSP.all.tids.__dict__.items():
        try:
            major_tid = value.tid
            if debug:
                print("MAJOR", key, major_tid)
            content = {"major": {"tid": major_tid, "name": key}}
            majorMinorMappings.update(
                {major_tid: content, key: content, str(major_tid): content}
            )
            for subkey, subvalue in value.__dict__.items():
                if subkey != "tid" and type(subvalue) == int:
                    if debug:
                        print("MINOR", subkey, subvalue)
                    content = {
                        "major": {"tid": major_tid, "name": key},
                        "minor": {"tid": subvalue, "name": subkey},
                    }
                    majorMinorMappings.update(
                        {subvalue: content, subkey: content, str(subvalue): content}
                    )
        except:
            pass
    return majorMinorMappings


def getTagStringFromTid(tid):
    majorMinorTopicMappings = getMajorMinorTopicMappings()
    topic = majorMinorTopicMappings.get(tid, None)
    tags = []
    if topic:
        majorTopic = topic.get("major", {}).get("name", None)
        minorTopic = topic.get("minor", {}).get("name", None)
        if majorTopic:
            tags.append(majorTopic)
            if minorTopic:
                tags.append(minorTopic)
    return ",".join(tags)


tid = 1
tagString = getTagStringFromTid(tid)
print(tid, tagString)
