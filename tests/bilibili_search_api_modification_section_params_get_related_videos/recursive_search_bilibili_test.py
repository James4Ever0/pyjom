import sys
import os

os.chdir("../../")
sys.path.append(".")
# ignore the global proxy now, we are not going to use that.
os.environ["http_proxy"] = ""
os.environ["https_proxy"] = ""

# metatopic = {
#     "optional": [
#         [
#             "狗狗",
#             "狗",
#             "汪汪",
#             "修勾",
#             "汪",
#             "狗子",
#         ],
#         ["喵喵", "猫", "猫咪", "喵"],
#     ],
#     "dynamic": [["可爱", "萌", "萌宠", "行为", "燃"]],
# }
dynamics = [["可爱", "萌", "萌宠"], ["行为", "燃"], ["搞笑", "逗比", "魔性"]]

cat_metatopic = {
    "static": [
        ["喵喵", "猫", "猫咪", "喵"],
    ],
    "dynamic": dynamics,
}

dog_metatopic = {
    "static": [
        [
            "狗狗",
            "狗",
            "汪汪",
            "修勾",
            "汪",
            "狗子",
        ],
    ],
    "dynamic": dynamics,
}

from pyjom.modules.topicGenerator.onlineTopicGenerator import getMetaTopicString
from bilibili_api import sync, search
from lazero.utils.tools import flattenUnhashableList  # one of my classic methods


def randomChoiceTagList(tag_list):
    import random

    selected_tags = random.sample(tag_list, 3)
    selected_tags = [random.sample(tags, min(len(tags), 2)) for tags in selected_tags]
    return list(set(selected_tags))


def getBilibiliPostMetadataForDogCat(sleepTime=2):
    import random

    selected_topic_list_dict = {"dog": [], "cat": []}
    core_topic_set = {*flattenUnhashableList(dog_metatopic)}
    randomTarget = lambda: random.choice(list(selected_topic_list_dict.keys()))
    dog_or_cat = randomTarget()

    description_list = []
    bgm_list = []
    title_list = []
    tag_list = []
    cover_list = []
    bvid_list = []

    def clearMyLists():
        nonlocal bvid_list, bgm_list, title_list, tag_list, cover_list, bvid_list, description_list
        description_list = []
        bgm_list = []
        title_list = []
        tag_list = []
        cover_list = []
        bvid_list = []

    getKeywords = {
        "dog": lambda: getMetaTopicString(dog_metatopic),
        "cat": lambda: getMetaTopicString(cat_metatopic),
    }
    BSP = search.bilibiliSearchParams()

    getDogTid = lambda: random.choice([BSP.all.tids.动物圈.tid, BSP.all.tids.动物圈.汪星人])
    getCatTid = lambda: random.choice([BSP.all.tids.动物圈.tid, BSP.all.tids.动物圈.喵星人])
    getTid = {"dog": getDogTid, "cat": getCatTid}

    getRandomPage = lambda: random.randint(1, 5)  # not so broad.
    # getRandomPage = lambda: random.randint(1, 50)  # broad range!
    orders = [
        BSP.all.order.最多点击,
        BSP.all.order.最多收藏,
        BSP.all.order.最新发布,
        BSP.all.order.最多弹幕,
        BSP.all.order.综合排序,
    ]
    randomOrder = lambda: random.choice(orders)
    while True:
        try:

            metatopicString = getKeywords[dog_or_cat]()

            print("METATOPIC STRING:", metatopicString)

            # we use video only search.

            result = sync(
                search.search_by_type(
                    keyword=metatopicString,
                    params={
                        "tids": getTid[dog_or_cat](),
                        "duration": BSP.all.duration._10分钟以下,
                        "order": randomOrder(),
                    },
                    page=getRandomPage(),
                    search_type=search.SearchObjectType.VIDEO,
                )
            )

            # print(result)
            # breakpoint()

            from searchDataParser import parseSearchVideoResult

            from pyjom.commons import checkMinMaxDict

            def updateMyLists(
                videoMetadata,
                duration_limit={"min": 70, "max": 5 * 60},
                play_limit={"min": 5000},debugTag="debug"
            ):
                nonlocal bvid_list, bgm_list, title_list, tag_list, cover_list, bvid_list, description_list  # use nonlocal instead in nested functions.
                (
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
                ) = videoMetadata
                # print("VIDEO_METADATA",videoMetadata)
                # breakpoint()
                if duration_seconds == None:
                    print(debugTag,"VIDEO_METADATA",videoMetadata)
                    breakpoint()
                elif play == None:
                    print(debugTag,"VIDEO_METADATA",videoMetadata)
                    breakpoint()
                if len(bgms) > 0:
                    bgm_list += bgms
                if checkMinMaxDict(duration_seconds, duration_limit):
                    if checkMinMaxDict(play, play_limit):
                        bvid_list += [bvid]
                        cover_list += [cover]
                        title_list += [title]  # this for topic modeling?
                        if description not in ["", None]:
                            description_list += [description]
                        if len(tags) > 0:
                            tag_list += [
                                tags
                            ]  # are you sure? this will make the tag_list into different shape!

            def updateMyListsWithIterable(
                iterable,
                duration_limit={"min": 70, "max": 5 * 60},
                play_limit={"min": 5000},
                debugTag = "debug"
            ):
                for videoMetadata in iterable:
                    updateMyLists(
                        videoMetadata,
                        duration_limit=duration_limit,
                        play_limit=play_limit,
                        debugTag = debugTag
                    )

            updateMyListsWithIterable(parseSearchVideoResult(result),'searchVideoResult')

            # do the related video search?
            if len(bvid_list) > 0:
                # get video info!
                from bilibili_api import video

                bvid = random.choice(bvid_list)
                v = video.Video(bvid=bvid)
                videoInfo = sync(v.get_info())
                from searchDataParser import parseVideoInfo

                primaryVideoInfo, secondaryVideoInfoList = parseVideoInfo(videoInfo)
                # for videoMetadata in secondaryVideoInfoList:
                updateMyListsWithIterable(secondaryVideoInfoList,debugTag = "secondaryVideoInfoList")
                # then we get related videos.
                result = sync(v.get_related())
                from searchDataParser import parseVideoRelated

                updateMyListsWithIterable(parseVideoRelated(result), debugTag = "videoRelated")

            # now what do you want? suggested keywords?
            suggested_queries = sync(
                search.get_suggest_keywords(keyword=metatopicString)
            )
            if type(suggested_queries) != list:
                suggested_queries = []
            # now we need to collect the keywords.
            # notice: we can only update this for selected topic like cat or dog. these keywords might not be shared.

            topic_modeling_source_sentences = suggested_queries.copy()
            for tags in tag_list:
                sentence = " ".join(tags)
                topic_modeling_source_sentences.append(sentence)
            for title in title_list:
                topic_modeling_source_sentences.append(title)

            from pyjom.modules.topicGenerator.onlineTopicGenerator import (
                topicModeling,
                topicWordSelection,
            )

            topics = topicModeling(topic_modeling_source_sentences, lang="zh")

            selectedWord = topicWordSelection(
                topics, core_topic_set, selected_topic_list_dict[dog_or_cat]
            )
            dog_or_cat = randomTarget()
            if selectedWord is not None:
                keywords = " ".join(
                    [getKeywords[dog_or_cat](), selectedWord]
                )  # for next iteration.
                print("REFRESHING KEYWORDS:", keywords)
            else:
                keywords = getKeywords[dog_or_cat]()
            # print(selected_topic_list_dict)
            # breakpoint()
            if len(title_list) > 3:
                if len(cover_list) > 3:
                    if len(tag_list) > 3:
                        if len(bgm_list) > 3:
                            # time to yield something.
                            mCover = random.choice(cover_list)
                            mTagSeries = randomChoiceTagList(
                                tag_list
                            )  # a collection of tags.
                            mTitle = random.choice(title_list)
                            mBgm = random.choice(bgm_list)
                            yield mCover, mTagSeries, mTitle, mBgm, dog_or_cat
                            clearMyLists()
        except:
            import time

            time.sleep(sleepTime)
            from lazero.utils.logger import traceError

            traceError("error when fetching metatopic")


if __name__ == "__main__":
    for videoMetadata in getBilibiliPostMetadataForDogCat():
        print("FETCHED VIDEO METADATA FOR PRODUCTION:")
        print(videoMetadata)
        mCover, mTagSeries, mTitle, mBgm, dog_or_cat = videoMetadata
        breakpoint()
