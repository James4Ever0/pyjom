import json
from bs4 import BeautifulSoup
from lazero.utils.logger import sprint

def traceError(errorMsg:str="error!"):
    import traceback
    traceback.print_exc()
    sprint(errorMsg)

def videoDurationStringToSeconds(durationString):
    durationString = durationString.strip()
    mList = durationString.split(":")[::-1]
    if len(mList) > 3:
        print("DURATION STRING TOO LONG")
        return None
    seconds = 0
    for index, elem in enumerate(mList):
        seconds += (60**index)*elem
    return seconds

def clearHtmlTags(htmlObject):
    a = BeautifulSoup(htmlObject, features='lxml')
    return a.text

test_subject = "search_all"

if test_subject == "search_all":
    with open("search_result_all.json", "r") as f:
        data = f.read()
        data = json.loads(data)
    results = data['result']
    for elem in results:
        try:
            if elem['result_type'] == 'video':
                for video in elem['data']:
                    # be warned cause all these things might fail.
                    try:
                        if video['type'] == 'video':
                            bvid = video['bvid']
                            tag = video['tag']
                            tags = tag.split(",")
                            categoryId = int(video['typeid'])
                            categoryName = int(video['typename'])
                            title = video['title'] # remove those markers, please?
                            title = clearHtmlTags(title)
                            duration = video['duration'] # this is not recommended. we need seconds.
                            play = video['play'] # select some hot videos.
                            cover = video['pic']
                            description = video['description']
                            duration_seconds = videoDurationStringToSeconds(duration)
                            for metadata in (bvid,tags,categoryId, categoryName,title, duration_seconds, play, cover, description):
                                print(metadata)
                            from lazero.utils.logger import sprint
                            sprint()
                    except:
                        traceError('error iterating video metadata')
                        continue
        except:
            traceError('error iterating data results')