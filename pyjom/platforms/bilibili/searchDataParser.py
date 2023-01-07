import json

# from bs4 import BeautifulSoup
from lazero.utils.logger import sprint
from pyjom.platforms.bilibili.utils import (
    # generatorToList,
    linkFixer,
    traceError,
    extractLinks,
    videoDurationStringToSeconds,
    getAuthorKeywords,
    clearHtmlTags,
    splitTitleTags,
    removeAuthorRelatedTags,
)


def parseVideoSearchItem(video, disableList: list = [], debug=False):
    from pyjom.platforms.bilibili.utils import detectAuthorRelatedKeywords
    bvid = video["bvid"]
    pubdate = video["pubdate"]
    if "author" not in disableList:
        author = video["author"]
        author_id = video[
            "mid"
        ]  # this is important. may let us able to find out the fans count.
    else:
        author = ""
        author_id = -1
    author_keywords = getAuthorKeywords(author)
    if "tag" not in disableList:
        tag = video["tag"]
        tags = tag.split(",")
        tags = [
            tag for tag in tags if not detectAuthorRelatedKeywords(tag, author_keywords)
        ]
    else:
        tags = []
    if "typeid" not in disableList and "typename" not in disableList:
        categoryId = int(video.get("typeid", video.get("type_id")))
        categoryName = video.get("typename", video.get("type_name"))
    else:
        categoryId = 0
        categoryName = ""
    title = video["title"]  # remove those markers, please?
    title = clearHtmlTags(title)
    title = removeAuthorRelatedTags(title, author)
    title, title_tags = splitTitleTags(
        title, author_keywords
    )  # use author for filtering unwanted title tags.
    duration = video["duration"]  # this is not recommended. we need seconds.
    play = video.get("play", video.get("view"))  # select some hot videos.
    cover = video["pic"]
    cover = linkFixer(cover)
    if "description" not in disableList:
        description = video.get("description", video.get("desc"))
        description = clearHtmlTags(description)
        description = removeAuthorRelatedTags(description, author)
    else:
        description = ""
    links_in_description, bgms, description = extractLinks(description)
    duration_seconds = videoDurationStringToSeconds(duration)
    resultTuple = (
        author,
        author_id,
        bvid,
        tags,
        categoryId,
        categoryName,
        title,
        duration_seconds,
        play,
        cover,
        description,
        links_in_description,
        bgms,
        title_tags,
        pubdate,
    )
    if debug:
        for metadata in resultTuple:
            print(metadata)
    from lazero.utils.logger import sprint

    if debug:
        sprint()
    return resultTuple


# you might want the creater's name, to filter out unwanted parts.


def iterateResultList(resultList, debug=False):
    for video in resultList:
        # be warned cause all these things might fail.
        try:
            if video["type"] == "video":
                yield parseVideoSearchItem(video, debug=debug)
        except:
            traceError("error iterating video metadata")
            continue


def parseSearchAllResult(data, debug=False):
    # if not generator:
    #     return generatorToList(parseSearchAllResult(data, debug=debug,generator=True))
    results = data["result"]
    for elem in results:
        try:
            if elem["result_type"] == "video":
                resultList = elem["data"]
                for videoMetadata in iterateResultList(resultList, debug=debug):
                    yield videoMetadata
        except:
            traceError("error iterating data results")


def parseSearchVideoResult(data, debug=False):
    # if not generator:
    #     return generatorToList(parseSearchVideoResult(data, debug=debug,generator=True))
    try:
        resultList = data["result"]
        try:
            for videoMetadata in iterateResultList(resultList, debug=debug):
                try:
                    yield videoMetadata
                except:
                    traceError("error iterating video metadata")
        except:
            traceError("error iterating result list")
    except:
        traceError("error parsing search video result")


def parseVideoInfo(videoInfo, debug=False):
    data = videoInfo
    # no tag out here.
    secondaryVideoInfoList = []
    data_copy = data.copy()
    data_copy.update({"author": data["owner"]["name"], "mid": data["owner"]["mid"]})
    data_copy.update(data["stat"])
    primaryVideoInfo = parseVideoSearchItem(
        data_copy, disableList=["tag", "typeid", "typename"], debug=debug
    )
    # videoInfoList.append(primaryVideoInfo)
    season = data.get("ugc_season", {})  # we only care about this thing.
    season_cover = season.get("cover", None)  # it could be noting.
    sections = season.get("sections", [])
    for section in sections:
        for episode in section["episodes"]:
            # print(episode.keys())
            # breakpoint()
            arc = episode["arc"]
            stat = arc["stat"]
            videoInfo = episode.copy()
            videoInfo.update(stat)
            videoInfo.update(arc)
            authorRelatedVideoInfo = parseVideoSearchItem(
                videoInfo,
                disableList=["tag", "typeid", "typename", "description", "author"],
                debug=debug,
            )  # author is the same as the original video.
            secondaryVideoInfoList.append(authorRelatedVideoInfo)
            # BV1Cb4y1s7em
            # []
            # 0

            # 这次真的燃起来了！！！
            # 217
            # 27911
            # http://i2.hdslb.com/bfs/archive/c5a0d18ee077fb6a4ac0970ccb0a3788e137d14f.jpg
    return primaryVideoInfo, secondaryVideoInfoList


def parseVideoRelated(videoRelatedData, debug=False):
    data = videoRelatedData
    # if not generator:
    #     return generatorToList(parseVideoRelated(data, debug=debug,generator=True))
    try:
        for videoInfo in data:
            try:
                videoInfo2 = videoInfo.copy()
                videoInfo2.update({"author": videoInfo["owner"]["name"]})
                videoInfo2.update({"mid": videoInfo["owner"]["mid"]})
                # also update the stat.
                videoInfo2.update(videoInfo["stat"])
                try:
                    yield parseVideoSearchItem(
                        videoInfo2,
                        disableList=["tag", "typeid", "typename"],
                        debug=debug,
                    )
                    # print(videoMetadata)
                except:
                    traceError()
            except:
                traceError()
    except:
        traceError()


if __name__ == "__main__":
    # fake tests.
    # test_subject = "search_video"
    # test_subject = "search_all"
    # test_subject = 'video_related'
    test_subject = "video_info"
    # test_subject = 'extract_links'
    if test_subject == "search_all":
        with open("search_result_all.json", "r") as f:
            data = f.read()
            data = json.loads(data)
        for mresult in parseSearchAllResult(data):
            print("RESULT:")
            sprint(mresult)
    elif test_subject == "search_video":
        with open("search_by_type_result_video.json", "r") as f:
            data = f.read()
            data = json.loads(data)
        for mresult in parseSearchVideoResult(data):
            print("VIDEO SEARCH RESULT:")
            sprint(mresult)
    elif test_subject == "video_info":
        with open("video_info.json", "r") as f:
            data = f.read()
            data = json.loads(data)
        primaryVideoInfo, secondaryVideoInfoList = parseVideoInfo(data)
        videoInfoList = [primaryVideoInfo] + secondaryVideoInfoList
        for mVideoInfo in videoInfoList:
            print(mVideoInfo)
            sprint()
    elif test_subject == "video_related":
        with open("video_related.json", "r") as f:
            data = f.read()
            data = json.loads(data)
        for videoMetadata in parseVideoRelated(data):
            print(videoMetadata)
            sprint()
    elif test_subject == "extract_links":
        description = (
            "http://www.toutiao.com/a6347649852365897986/ 男子送走从小养大的狗，狗狗用泪汪汪的眼神看着他\n"
            + "https://www.youtube.com/watch?v=r724w57oXyU"
            + " https://www.youtube.com/shorts/UYCy8HD1C7o"
        )
        links, desc = extractLinks(description)
        print(links)
        print(desc)
    else:
        raise Exception("unknown test_subject:", test_subject)
