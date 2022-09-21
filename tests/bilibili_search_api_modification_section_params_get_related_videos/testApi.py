from bilibili_api import sync, search

BSP = search.bilibiliSearchParams()

# result = sync(
#     search.search(
#         keyword="汪汪",
#         params={"tids": BSP.all.tids.动物圈.tid, "duration": BSP.all.duration._10分钟以下},
#         page=1
#     )
# )

# print(result)
# how to get suggested keyword?

# suggested_keyword = sync(search.get_suggest_keywords(keyword = "汪汪"))
# print(suggested_keyword)
# you might want to split this.
# this is not deterministic.

# ['汪汪队立大功 第二季 中文配音', '汪汪队立大功', '汪汪队立大功神威狗狗', '汪汪队', '特别任务 汪汪队立大功 冒险湾的一天', '雀魂汪汪录', '汪汪公主biu', '汪汪来透剧', '汪汪在亚美尼亚', '汪汪队立大功 第一季 中文配音']
# ['汪汪队立大功', '汪汪队', '汪汪队立大功 第一季 中文配音', '汪汪队立大功 第二季 中文配音', '汪汪录', '汪汪队立大功大电影', '汪汪队立大功中文', '汪汪队立大功神威狗狗', '汪汪汪', '汪汪队中文']

import json

# result_str = json.dumps(result, ensure_ascii=False, indent=4)
# with open("search_result_all.json",'w+') as f:
#     f.write(result_str)

# get video info
from bilibili_api import video

bvid = "BV1iw411Z7xt"
v = video.Video(bvid=bvid)

# info=sync(v.get_info())
# # print(info)
# with open('video_info.json', 'w+') as f:
#     f.write(json.dumps(info, indent=4, ensure_ascii=False))
# -> pages to access all parted videos.
# -> ugc_season to get maker collected seasons.

# # video tags
# able to get from search

# related videos
# related = sync(v.get_related())

# with open('video_related.json', 'w+') as f:
#     f.write(json.dumps(related, indent=4, ensure_ascii=False))

# search video

result = sync(
    search.search_by_type(
        keyword="汪汪",
        params={"tids": BSP.all.tids.动物圈.tid, "duration": BSP.all.duration._10分钟以下},
        page=1,
        search_type=search.SearchObjectType.VIDEO,
    )
)

with open('search_by_type_result_video.json','w+') as f:
    f.write(json.dumps(result, indent=4, ensure_ascii=False))

# with open("search_result_all.json", "r") as f:
#     data = f.read()
#     data = json.loads(data)
