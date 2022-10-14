# not sure if it relates.

from baiduspider import BaiduSpider
spider=BaiduSpider()
from pprint import pprint
query = "绝对领域"
result = spider.search_pic(query, pn= 1) # are we fucked?
# yeah we have result.
print(result)
result.plain
breakpoint()
# 'title', 'url', 'host'
# can we search for gif?