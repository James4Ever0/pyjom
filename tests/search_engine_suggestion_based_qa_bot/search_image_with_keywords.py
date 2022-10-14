# not sure if it relates.

from baiduspider import BaiduSpider
spider=BaiduSpider()
from pprint import pprint
query = "绝对领域"
result = spider.search_img(query, pn= 1)
print(result)
breakpoint()