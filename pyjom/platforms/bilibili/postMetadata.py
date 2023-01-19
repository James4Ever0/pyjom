from pyjom.commons import *
import cv2
from pyjom.modules.topicGenerator.onlineTopicGenerator import getMetaTopicString
from bilibili_api import sync, search
from lazero.utils.tools import flattenUnhashableList  # one of my classic methods
from lazero.utils.logger import sprint

# TODO: you know the drill. if it really contains nonacceptable characters (currently, must be some rule changes), you use Notofu font for rendering and OCR for recognition.
# well you might want tesseract.
# i suspect this change is due to language models used in bilibili's system
from pyjom.languagetoolbox import filterNonChineseOrEnglishOrJapaneseCharacters

def filterTitleWithCoreTopicSet(title, core_topic_set, debug=False):
    value = False
    for core_topic in core_topic_set:
        if core_topic in title:
            value = True
            break
    if debug:
        print("TITLE:", title)
        print("CORE TOPIC SET:", core_topic_set)
        print("VALUE:", value)
        breakpoint()
    return value


def filterTitleListWithCoreTopicSet(titleList, core_topic_set, debug=False):
    newTitleList = []
    for title in titleList:
        result = filterTitleWithCoreTopicSet(title, core_topic_set)
        if result:
            newTitleList.append(title)
    if debug:
        print("TITLE LIST:", titleList)
        print("CORE TOPIC SET:", core_topic_set)
        sprint("NEW TITLE LIST:", newTitleList)
    return newTitleList


def randomChoiceTagList(
    tag_list, selected_tag_groups=3, selected_tag_per_group=2, pop=True
):
    import random

    if not pop:
        selected_tags = random.sample(tag_list, selected_tag_groups)
    else:
        selected_tags = [
            shuffleAndPopFromList(tag_list) for _ in range(selected_tag_groups)
        ]
    selected_tags = [
        random.sample(tags, min(len(tags), selected_tag_per_group))
        for tags in selected_tags
    ]
    # flatten this thing.
    selected_tags = flattenUnhashableList(selected_tags)
    return list(set(selected_tags))


from typing import Literal
from pyjom.imagetoolbox import resizeImageWithPadding


def getCoverTargetFromCoverListDefault(
    cover_list,
    dog_or_cat_original,
    input_width: int = 1200,
    output_width: int = 1920,
    filter_function=lambda image: image,
    histogramMatch=True,
    delta=0.2,
    flip: Literal[True, False, "random"] = True,
):  # default function does not process this tag.
    import random

    if flip == "random":
        flip = random.choice([True, False])
    # random.shuffle(cover_list)
    # reference_histogram_cover = random.choice(cover_list)
    reference_histogram_cover = shuffleAndPopFromList(cover_list)

    cover_target = None

    # for cover in cover_list:
    while len(cover_list) > 0:
        cover = shuffleAndPopFromList(cover_list)
        import os

        os.environ["http"] = ""
        os.environ["https"] = ""
        from pyjom.imagetoolbox import (
            imageLoader,
            # imageDogCatCoverCropAdvanced,
            imageHistogramMatch,
        )

        image = imageLoader(cover)
        # downscale this image first.
        image = resizeImageWithPadding(
            image, input_width, None, border_type="replicate"
        )  # are you sure? it is just a cover image.
        cropped_image = filter_function(
            image
        )  # we should do something to the filter function!
        if cropped_image is not None:
            if histogramMatch:
                cropped_image = imageHistogramMatch(
                    cropped_image, reference_histogram_cover, delta=delta
                )
            if flip:
                cropped_image = cv2.flip(cropped_image, 1)
            cover_target = cropped_image
            break
    if cover_target is not None:
        cover_target = resizeImageWithPadding(
            cover_target, output_width, None, border_type="replicate"
        )  # this is strange.
    return cover_target


def getCoverTargetFromCoverListForDogCat(cover_list, dog_or_cat_original):
    from pyjom.imagetoolbox import (
        # imageLoader,
        imageDogCatCoverCropAdvanced,
        # imageHistogramMatch,
    )

    return getCoverTargetFromCoverListDefault(
        cover_list,
        dog_or_cat_original,
        filter_function=lambda image: imageDogCatCoverCropAdvanced(
            image,
            yolov5_confidence_threshold=0.27,  # you made it smaller.
            dog_or_cat=dog_or_cat_original,  # already configured. no need to do shit.
            area_threshold=0.30,  # 0.7 # could be smaller.
            corner=False,
        ),
    )


BSP = search.bilibiliSearchParams()
import random

from typing import Callable

def getBilibiliPostMetadata(
    sleepTime=2,
    customParaphraser:Union[Callable,None]=None,
    getMetatopic={},
    bgmCacheSetName: Union[str, None] = "bilibili_cached_bgm_set",
    getTids={},  # these two are not specified here.
    genericTids:list[int]=[],
    orders=[
        BSP.all.order.最多点击,
        BSP.all.order.最多收藏,
        BSP.all.order.最新发布,
        BSP.all.order.最多弹幕,
        BSP.all.order.综合排序,
    ],
    pageIndexRange=(1, 5),
    duration=BSP.all.duration._10分钟以下,
    lang="zh",
    duration_limit={"min": 70, "max": 5 * 60},
    play_limit={"min": 10000},
    titleLengthLimit={"min": 7, "max": 17},
    getCoverTargetFromCoverList=getCoverTargetFromCoverListDefault,  # what is the default process?
    bgmCacheAutoPurge=False,
):
    if bgmCacheSetName and bgmCacheAutoPurge:
        removeRedisValueByKey(bgmCacheSetName)
    selected_topic_list_dict = {key: [] for key in getMetatopic.keys()}
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
        key: lambda: getMetaTopicString(value) for key, value in getMetatopic.items()
    }

    # getDogTid = lambda: random.choice([BSP.all.tids.动物圈.tid, BSP.all.tids.动物圈.汪星人])
    # getCatTid = lambda: random.choice([BSP.all.tids.动物圈.tid, BSP.all.tids.动物圈.喵星人])
    # getTid = {"dog": getDogTid, "cat": getCatTid}
    getTid = {key: lambda: random.choice(value) for key, value in getTids.items()}
    getTargetTid = {key: lambda: random.choice([v for v in value if v not in genericTids]) for key, value in getTids.items()}

    getRandomPage = lambda: random.randint(*pageIndexRange)  # not so broad.
    # getRandomPage = lambda: random.randint(1, 50)  # broad range!

    randomOrder = lambda: random.choice(orders)
    while True:
        try:
            core_topic_set = {
                *flattenUnhashableList(
                    [value for key, value in getMetatopic[dog_or_cat].items()]
                )
            }

            static_core_topic_list = flattenUnhashableList(
                getMetatopic[dog_or_cat]["static"]
            )

            metatopicString = getKeywords[dog_or_cat]()

            print("METATOPIC STRING:", metatopicString)

            # we use video only search.
            search_tid = getTid[dog_or_cat]()
            target_tid = getTargetTid[dog_or_cat]()

            result = sync(
                search.search_by_type(
                    keyword=metatopicString,
                    params={
                        "tids": search_tid,
                        "duration": duration,
                        "order": randomOrder(),
                    },
                    page=getRandomPage(),
                    search_type=search.SearchObjectType.VIDEO,
                )
            )

            # print(result)
            # breakpoint()

            from pyjom.platforms.bilibili.searchDataParser import parseSearchVideoResult

            from pyjom.mathlib import checkMinMaxDict

            def updateMyLists(
                videoMetadata,
                duration_limit={"min": 70, "max": 5 * 60},
                titleLengthLimit={"min": 7, "max": 17},
                play_limit={"min": 10000},
                debugTag="debug",
            ):
                nonlocal bvid_list, bgm_list, title_list, tag_list, cover_list, bvid_list, description_list, static_core_topic_list  # use nonlocal instead in nested functions.
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
                    pubdate,
                ) = videoMetadata
                # print("VIDEO_METADATA",videoMetadata)
                # breakpoint()
                if not checkMinMaxDict(len(title), titleLengthLimit):
                    return
                if not filterTitleWithCoreTopicSet(title, static_core_topic_list):
                    return
                if len(tags) > 0:
                    tagContainStaticCoreTopicFlags = [
                        int(filterTitleWithCoreTopicSet(tag, static_core_topic_list))
                        for tag in tags
                    ]
                    mTagFlag = sum(tagContainStaticCoreTopicFlags) > 0
                    if not mTagFlag:
                        return
                else:
                    return
                if duration_seconds == None:
                    print(debugTag, "VIDEO_METADATA", videoMetadata)
                    breakpoint()
                elif play == None:
                    print(debugTag, "VIDEO_METADATA", videoMetadata)
                    breakpoint()
                if len(bgms) > 0:
                    bgm_list += bgms
                try:
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
                except:
                    traceError()
                    breakpoint()

            def updateMyListsWithIterable(
                iterable,
                duration_limit={"min": 70, "max": 5 * 60},
                play_limit={"min": 10000},
                titleLengthLimit={"min": 7, "max": 17},
                debugTag="debug",
            ):
                for videoMetadata in iterable:
                    updateMyLists(
                        videoMetadata,
                        duration_limit=duration_limit,
                        play_limit=play_limit,
                        titleLengthLimit=titleLengthLimit,
                        debugTag=debugTag,
                    )

            updateMyListsWithIterable(
                parseSearchVideoResult(result),
                duration_limit=duration_limit,
                play_limit=play_limit,
                titleLengthLimit=titleLengthLimit,
                debugTag="searchVideoResult",
            )

            # do the related video search?
            if len(bvid_list) > 0:
                # get video info!
                from bilibili_api import video

                bvid = random.choice(bvid_list)
                v = video.Video(bvid=bvid)
                videoInfo = sync(v.get_info())
                from pyjom.platforms.bilibili.searchDataParser import parseVideoInfo

                primaryVideoInfo, secondaryVideoInfoList = parseVideoInfo(videoInfo)
                # for videoMetadata in secondaryVideoInfoList:
                updateMyListsWithIterable(
                    secondaryVideoInfoList, debugTag="secondaryVideoInfoList"
                )
                # then we get related videos.
                result = sync(v.get_related())
                from pyjom.platforms.bilibili.searchDataParser import parseVideoRelated

                # import json

                # print(json.dumps(result, indent=4, ensure_ascii=False))
                # print('parsing related video info')
                # breakpoint()

                updateMyListsWithIterable(
                    parseVideoRelated(result), debugTag="videoRelated"
                )

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

            topics = topicModeling(topic_modeling_source_sentences, lang=lang)

            selectedWord = topicWordSelection(
                topics, core_topic_set, selected_topic_list_dict[dog_or_cat]
            )
            dog_or_cat_original = dog_or_cat
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

            filtered_title_list = filterTitleListWithCoreTopicSet(
                title_list, static_core_topic_list
            )  # could be enhabced with CLIP
            filtered_description_list = filterTitleListWithCoreTopicSet(
                description_list, static_core_topic_list
            )
            # filtered_title_list = filterTitleListWithCoreTopicSet(title_list, core_topic_set) # could be enhabced with CLIP
            # store the bgm elsewhere?
            # where? you store it where?

            if bgmCacheSetName:  # no matter what you got to do this.
                for item in bgm_list:
                    addToRedisCachedSet(item, bgmCacheSetName)
            if len(filtered_description_list) > 3:
                if len(filtered_title_list) > 3:
                    if len(cover_list) > 3:
                        if len(tag_list) > 3:
                            if len(bgm_list) > 3:
                                # time to yield something.
                                # detect this thing!
                                # filtered_cover_list = []
                                # this method needs to change. the cover_list.
                                cover_target = getCoverTargetFromCoverList(
                                    cover_list,
                                    dog_or_cat_original,  # this is the label of the selected metatopic. might be useful.
                                )
                                # this is a general thing.
                                # r = requests.get(cover)
                                # content = r.content
                                # # corrupted or not?
                                # image = cv2.imdecode(content, cv2.IMREAD_COLOR)
                                # mCover = random.choice(filtered_cover_list) # what is this cover list?
                                # mDescription = random.choice(filtered_description_list)
                                mDescription = shuffleAndPopFromList(
                                    filtered_description_list
                                )
                                if cover_target is not None:
                                    # you want to pop these things?
                                    # clearly a list of strings
                                    mTagSeries = randomChoiceTagList(
                                        tag_list, pop=True
                                    )  # a collection of tags.
                                    mTagSeries = [filterNonChineseOrEnglishOrJapaneseCharacters(tag) for tag in mTagSeries]
                                    # mTitle = random.shuffle(filtered_title_list)
                                    mTitle = shuffleAndPopFromList(filtered_title_list)
                                    # mBgm = random.choice(bgm_list)
                                    # really serious?
                                    mBgm = shuffleAndPopFromList(bgm_list)

                                    # you enable this paraphrase option here.
                                    if customParaphraser:
                                        mTitle = customParaphraser(mTitle)
                                        mDescription = customParaphraser(mDescription)
                                    yield (cover_target, mTagSeries, filterNonChineseOrEnglishOrJapaneseCharacters(mTitle), mBgm, filterNonChineseOrEnglishOrJapaneseCharacters(mDescription), dog_or_cat_original, 
                                    target_tid
                                    # search_tid
                                    )  # one additional return value
                                    # the search tid is not good.
                                    # we must remove the generic tid.
                                    clearMyLists()
        except:
            import time

            time.sleep(sleepTime)
            from lazero.utils.logger import traceError

            traceError("error when fetching metatopic")


def getBilibiliPostMetadataForDogCat(
    dog_or_cat: Literal["dog", "cat"] = "dog",
    bgmCacheSetName="bilibili_cached_bgm_set",
    bgmCacheAutoPurge=False,
    customParaphraser:Union[Callable, None]=None
):
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
    getMetatopic = {
        "dog": dog_metatopic,
        "cat": cat_metatopic,
    }
    # bullshit.
    # must use subcategories.
    getTids = {
        "dog": [BSP.all.tids.动物圈.tid, BSP.all.tids.动物圈.汪星人],
        "cat": [BSP.all.tids.动物圈.tid, BSP.all.tids.动物圈.喵星人],
    }
    genericTids = [BSP.all.tids.动物圈.tid] # these tids cannot be used for video posting.
    ## then the decision.
    getMetatopic = {
        key: value for key, value in getMetatopic.items() if key == dog_or_cat
    }
    getTids = {key: value for key, value in getTids.items() if key == dog_or_cat}

    return getBilibiliPostMetadata(  # this is a premature version. the deeplearning version might interest you more. but how the fuck i can integrate DL into this shit?
        getMetatopic=getMetatopic,
        getTids=getTids,
        getCoverTargetFromCoverList=getCoverTargetFromCoverListForDogCat,
        bgmCacheSetName=bgmCacheSetName,
        bgmCacheAutoPurge=bgmCacheAutoPurge,
        customParaphraser = customParaphraser,
        genericTids=genericTids # cannot used for upload tid specification.
    )
