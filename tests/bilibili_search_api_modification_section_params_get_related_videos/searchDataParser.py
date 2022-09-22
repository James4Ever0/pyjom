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

def extractLinks(description):
    """Extract and remove links in description"""
    import re
    # notice, we don't need to go wild here. we just want the title and the cover, and the tags.
    expression = r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
    # expr = re.compile(expression)
    links = re.findall(expression,description)
    if links == None:
        links = []
    desc_without_link = re.sub(expression, "", description)
    desc_without_link = "\n".join([x.replace("\n",'').strip() for x in desc_without_link.split("\n")])
    return links, desc_without_link

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

def parseVideoSearchItem(video, disableList:list=[], debug=False):
    bvid = video['bvid']
    if 'author' not in disableList:
        author = video['author']
        author_id = video['mid']
    else:
        author = ""
        author_id = -1
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
    if 'description' not in disableList:
        description = video.get('description', video.get('desc'))
        description = clearHtmlTags(description)
    else:
        description = ""
    links_in_description, description = extractLinks(description)
    duration_seconds = videoDurationStringToSeconds(duration)
    if debug:
        for metadata in (author,author_id,bvid,tags,categoryId, categoryName,title, duration_seconds, play, cover, description,links_in_description):
            print(metadata)
    from lazero.utils.logger import sprint
    if debug:
        sprint()
    return author,author_id,bvid,tags,categoryId, categoryName,title, duration_seconds, play, cover, description,links_in_description

# you might want the creater's name, to filter out unwanted parts.

def iterateResultList(resultList, debug=False):
    for video in resultList:
        # be warned cause all these things might fail.
        try:
            if video['type'] == 'video':
                yield parseVideoSearchItem(video)
        except:
            traceError('error iterating video metadata')
            continue

def parseSearchAllResult(data, debug=False):
    results = data['result']
    for elem in results:
        try:
            if elem['result_type'] == 'video':
                resultList = elem['data']
                yield iterateResultList(resultList, debug=False)
        except:
            traceError('error iterating data results')

def parseSearchVideoResult(data):
    resultList = data['result']
    iterateResultList(resultList)

if __name__ == "__main__":
    # test_subject = "search_video"
    test_subject = "search_all"
    # test_subject = 'video_related'
    # test_subject = 'video_info'
    # test_subject = 'extract_links'

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
        data_copy = data.copy()
        data_copy.update({"author":data['owner']['name'], "mid":data['owner']['mid']})
        data_copy.update(data['stat'])
        parseVideoSearchItem(data_copy, disableList=['tag','typeid','typename'])
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
                parseVideoSearchItem(videoInfo, disableList = ['tag', 'typeid','typename','description','author']) # author is the same as the original video.
                # BV1Cb4y1s7em
                # []
                # 0

                # 这次真的燃起来了！！！
                # 217
                # 27911
                # http://i2.hdslb.com/bfs/archive/c5a0d18ee077fb6a4ac0970ccb0a3788e137d14f.jpg
    elif test_subject == "video_related":
        with open("video_related.json", "r") as f:
            data = f.read()
            data = json.loads(data)
        try:
            for videoInfo in data:
                try:
                    videoInfo2 =videoInfo.copy()
                    videoInfo2.update({'author': videoInfo['owner']['name']})
                    videoInfo2.update({'mid': videoInfo['owner']['mid']})
                    try:
                        parseVideoSearchItem(videoInfo2,disableList = ['tag','typeid','typename'])
                    except:
                        traceError()
                except:
                    traceError()
        except:
            traceError()
    elif test_subject == 'extract_links':
        description = "http://www.toutiao.com/a6347649852365897986/ 男子送走从小养大的狗，狗狗用泪汪汪的眼神看着他\n"+"https://www.youtube.com/watch?v=r724w57oXyU"+ " https://www.youtube.com/shorts/UYCy8HD1C7o"
        links, desc = extractLinks(description)
        print(links)
        print(desc)
    else:
        raise Exception("unknown test_subject:", test_subject)