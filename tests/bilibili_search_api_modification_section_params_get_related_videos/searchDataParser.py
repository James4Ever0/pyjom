import json
from bs4 import BeautifulSoup
from lazero.utils.logger import sprint

def linkFixer(link,prefix="https:"):
    if link.startswith("//"):
        return prefix+link
    return link

def traceError(errorMsg:str="error!", _breakpoint:bool=False):
    import traceback
    traceback.print_exc()
    sprint(errorMsg)
    if _breakpoint:
        return breakpoint()

def videoDurationStringToSeconds(durationString):
    durationString = durationString.strip()
    mList = durationString.split(":")[::-1]
    if len(mList) > 3:
        print("DURATION STRING TOO LONG")
        return None
    seconds = 0
    for index, elem in enumerate(mList):
        elem = int(elem)
        seconds += (60**index)*elem
    return seconds

def clearHtmlTags(htmlObject):
    a = BeautifulSoup(htmlObject, features='lxml')
    return a.text

def iterateResultList(resultList):
    for video in resultList:
        # be warned cause all these things might fail.
        try:
            if video['type'] == 'video':
                bvid = video['bvid']
                tag = video['tag']
                tags = tag.split(",")
                categoryId = int(video['typeid'])
                categoryName = video['typename']
                title = video['title'] # remove those markers, please?
                title = clearHtmlTags(title)
                duration = video['duration'] # this is not recommended. we need seconds.
                play = video['play'] # select some hot videos.
                cover = video['pic']
                cover = linkFixer(cover)
                description = video['description']
                duration_seconds = videoDurationStringToSeconds(duration)
                for metadata in (bvid,tags,categoryId, categoryName,title, duration_seconds, play, cover, description):
                    print(metadata)
                from lazero.utils.logger import sprint
                sprint()
        except:
            traceError('error iterating video metadata')
            continue

def parseSearchAllResult(data):
    results = data['result']
    for elem in results:
        try:
            if elem['result_type'] == 'video':
                resultList = elem['data']
                iterateResultList(resultList)
        except:
            traceError('error iterating data results')

def parseSearchVideoResult(data):
    

test_subject = "search_video"
# test_subject = "search_all"

if test_subject == "search_all":
    with open("search_result_all.json", "r") as f:
        data = f.read()
        data = json.loads(data)
    parseSearchAllResult(data)
elif test_subject == "search_video":
    with open("search_by_type_result_video.json", "r") as f:
        data = f.read()
        data = json.loads(data)
    parseSearchResult(data)
else:
    raise Exception("unknown test_subject:", test_subject)