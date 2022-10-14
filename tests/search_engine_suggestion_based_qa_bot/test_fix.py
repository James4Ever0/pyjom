query = "python有个问题想请教一下 为什么我这个函数跑不通"

from baiduspider import BaiduSpider
spider=BaiduSpider()
from pprint import pprint

result = spider.search_web(query, pn= 1)
print(result.plain)
# change the div class name.
# change 'result-op' into 'result' at line 153
# file: /usr/local/lib/python3.9/dist-packages/baiduspider/parser/__init__.py:153
# https://github.com/BaiduSpider/BaiduSpider/pull/151
# https://github.com/BaiduSpider/BaiduSpider/pull/151/files
# breakpoint()
# result.normal[0].url
# also update the news extraction logic:
# https://github.com/BaiduSpider/BaiduSpider/pull/127/files
# 'des', 'origin', 'plain', 'snapshot', 'time', 'title', 'url'