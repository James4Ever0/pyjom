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

cat_metatopic = {
    "static": [
        ["喵喵", "猫", "猫咪", "喵"],
    ],
    "dynamic": [["可爱", "萌", "萌宠", "行为", "燃"]],
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
    "dynamic": [["可爱", "萌", "萌宠", "行为", "燃"]],
}

from pyjom.modules.topicGenerator.onlineTopicGenerator import getMetaTopicString
from bilibili_api import sync, search

dog_metatopicString = getMetaTopicString(dog_metatopic)
import random
getDogTid = lambda: random.choice([BSP.all.tids.动物圈.tid,BSP.all.tids.动物圈.汪星人])
getRandomPage = lambda: random.randint(1,50)
print(dog_metatopicString)

# we use video only search.

BSP = search.bilibiliSearchParams()

result = sync(
    search.search_by_type(
        keyword=dog_metatopicString,
        params={"tids": getDogTid(), "duration": BSP.all.duration._10分钟以下},
        page=getRandomPage(),
        search_type=search.SearchObjectType.VIDEO,
    )
)

from searchDataParser import parseSearchVideoResult

description_list = []
bgm_list = []
title_list = []
tag_list = []
cover_list = []
bvid_list = []


from pyjom.commons import checkMinMaxDict

def updateMyListsWithIterable(iterable,duration_limit = {"min":70, 'max':5*60},play_limit = {"min": 10000}):
    

def updateMyLists(videoMetadata,duration_limit = {"min":70, 'max':5*60},play_limit = {"min": 10000}):
    global bvid_list, bgm_list, title_list, tag_list, cover_list, bvid_list, description_list # use nonlocal instead in nested functions.
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
    ) = videoMetadata
    if checkMinMaxDict(duration_seconds, duration_limit):
        if checkMinMaxDict(play, play_limit):
            bvid_list += [bvid]
            bgm_list += bgms
            cover_list += [cover]
            title_list += [title] # this for topic modeling?
            description_list += [description]
            tag_list += tags # this?

for videoMetadata in parseSearchVideoResult(result):
    updateMyLists(videoMetadata)

# do the related video search?
if len(bvid_list)>0:
    # get video info!
    from bilibili_api import video
    bvid = random.choice(bvid_list)
    v = video.Video(bvid=bvid)
    videoInfo = sync(v.get_info())
    from searchDataParser import parseVideoInfo
    primaryVideoInfo, secondaryVideoInfoList = parseVideoInfo(videoInfo)
    for videoMetadata in secondaryVideoInfoList:
        updateMyLists(videoMetadata)
    # then we get related videos.
    result = sync(v.get_related())
    from searchDataParser import parseVideoRelated
    for videoMetadata in parseVideoRelated(result):