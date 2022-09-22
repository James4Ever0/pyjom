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

duration_limit = {"min":70, 'max':5*60}
play_limit = {"min": 10000}
from pyjom.commons import checkMinMaxDict

for videoMetadata in parseSearchVideoResult(result):
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
            bgm_list += bgms
            cover_list += [cover]
            title_list += [title] # this for topic modeling?
            description_list += [description]
            tag_list += tags # this?