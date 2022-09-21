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

suggested_keyword = sync(search.)

import json
# result_str = json.dumps(result, ensure_ascii=False, indent=4)
# with open("search_result_all.json",'w+') as f:
#     f.write(result_str)

with open("search_result_all.json",'r') as f:
    data = f.read()
    data = json.loads(data)