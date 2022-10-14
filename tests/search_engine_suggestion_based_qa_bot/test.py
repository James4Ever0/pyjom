# we need suggestion, related topics, also search results.
# can be used in title generation.

# title/message as query (-> keyword -> suggested query) -> search results -> extract response/title

# suggestion, trending topics/keywords

# black hat seo, https://www.blackhatworld.com/forums/black-hat-seo.28/

# paste your link 'elsewhere' 自动评论 自动发布信息 私信, submit your link to search engine somehow, visit your link from search engine somehow

# seo without website

# write a blog on github?

# create short links and submit them to search engine

# get query count, perform n-gram analysis
# https://www.aeripret.com/ngrams-analysis-seo/

# https://www.pemavor.com/seo-keyword-clustering-with-python/

# i have bookmarked links for further use on macbook chrome.

query = "python有个问题想请教一下 为什么我这个函数跑不通"

from baiduspider import BaiduSpider
spider=BaiduSpider()
from pprint import pprint

result = spider.search_web(query, pn= 1)
# print(result)
# nothing returned.
import random
# result.related 
related = result.related
next_query = random.choice(related)
# next_query = 'python'
print('next query: %s' % next_query)
from baidusearch.baidusearch import search

# the abstract is bad
# use toapi to make website into api.
# https://github.com/gaojiuli/toapi

results = search(next_query, num_results=20)  # returns 20 or less results
# # next_result = spider.search_web(next_query, pn= 1)
# # print(next_result)
# # print(results) #this is working.
# # breakpoint()
# import parse

# use jina? hahaha...
import json
string = json.dumps(results, ensure_ascii=False, indent=4)
with open('result_baidu.json', 'w+') as f:
    f.write(string)
# no search result! fuck.
# what is going on?

# 'baike', 'blog', 'calc', 'gitee', 'music', 'news', 'normal', 'pages', 'plain', 'related', 'tieba', 'total', 'video'
