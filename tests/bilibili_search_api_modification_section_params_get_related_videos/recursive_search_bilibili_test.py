
import sys
import os

os.chdir("../../")
sys.path.append(".")
# ignore the global proxy now, we are not going to use that.
os.environ["http_proxy"] = ""
os.environ["https_proxy"] = ""

metatopic = {
    "optional": [
        [
            "狗狗",
            "狗",
            "汪汪",
            "修勾",
            "汪",
            "狗子",
        ],
        ["喵喵", "猫", "猫咪", "喵"],
    ],
    "dynamic": [["可爱", "萌", "萌宠", "行为", "燃"]],
}

from pyjom.modules.topicGenerator.onlineTopicGenerator import getMetaTopicString

metatopicString = getMetaTopicString(metatopic)

print(metatopicString)

from bilibili_api import sync, search

BSP = search.bilibiliSearchParams()


# result = sync(
#     search.search(
#         keyword="汪汪",
#         params={"tids": BSP.all.tids.动物圈.tid, "duration": BSP.all.duration._10分钟以下},
#         page=1
#     )
# )
