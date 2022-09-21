import json
from bs4 import BeautifulSoup
from lazero.utils.logger import sprint

def linkFixer(link,prefix="http:"):
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
    if type(durationString) == int:
        return durationString # not string at all.
    if type(durationString) !=str:
        print('unknown durationString type: %s' % type(durationString))
        return None
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

def parseVideoSearchItem(video, disableList:list=[]):
    bvid = video['bvid']
    if 'tag' not in disableList:
        tag = video['tag']
        tags = tag.split(",")
    else:
        tags = []
    if 'typeid' not in disableList and 'typename' not in disableList:
        categoryId = int(video.get('typeid',video.get('type_id')))
        categoryName = video.get('typename', video.get('type_name'))
    else:
        categoryId = 0
        categoryName = ""
    title = video['title'] # remove those markers, please?
    title = clearHtmlTags(title)
    duration = video['duration'] # this is not recommended. we need seconds.
    play = video.get('play',video.get('view')) # select some hot videos.
    cover = video['pic']
    cover = linkFixer(cover)
    description = video.get('description']
    duration_seconds = videoDurationStringToSeconds(duration)
    for metadata in (bvid,tags,categoryId, categoryName,title, duration_seconds, play, cover, description):
        print(metadata)
    from lazero.utils.logger import sprint
    sprint()

def iterateResultList(resultList):
    for video in resultList:
        # be warned cause all these things might fail.
        try:
            if video['type'] == 'video':
                parseVideoSearchItem(video)
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
    resultList = data['result']
    iterateResultList(resultList)

# test_subject = "search_video"
# test_subject = "search_all"
test_subject = 'video_info'

if test_subject == "search_all":
    with open("search_result_all.json", "r") as f:
        data = f.read()
        data = json.loads(data)
    parseSearchAllResult(data)
elif test_subject == "search_video":
    with open("search_by_type_result_video.json", "r") as f:
        data = f.read()
        data = json.loads(data)
    parseSearchVideoResult(data)
elif test_subject =='video_info':
    with open("video_info.json", "r") as f:
        data = f.read()
        data = json.loads(data)
    # no tag out here.
    season = data['ugc_season'] # we only care about this thing.
    season_cover = season['cover']
    sections = season['sections']
    for section in sections:
        for episode in section['episodes']:
            # print(episode.keys())
            # breakpoint()
            arc = episode['arc']
            stat = arc['stat']
            videoInfo=episode.copy()
            videoInfo.update(stat)
            videoInfo.update(arc)
            parseVideoSearchItem(videoInfo, disableList = ['tag'])
else:
    raise Exception("unknown test_subject:", test_subject)