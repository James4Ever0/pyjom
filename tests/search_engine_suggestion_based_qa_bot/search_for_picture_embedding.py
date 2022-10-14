# actually the clip model does well for this.
# though you want to use bm25 based textrank

image = "prettyGirl.jpeg" # girl image

from PicImageSearch.sync import BaiDu

baidu = BaiDu()
result = baidu.search(file=image)
# print(result)
# better not to query 'ajax' unless you want to get banned.
# breakpoint()
for elem in result.raw:
    thumbnail = elem.get('thumbnail')
    sim = elem.get('similarity')
    title = elem.get('title')
    # url is not necessary since we 
# ['origin', 'raw', 'url']
# result.raw[0].url is the original url. however you won't get the picture.
# result.raw[0].thumbnail
# 'origin', 'similarity', 'thumbnail', 'title', 'url'
# result.raw[0].origin['ajaxUrl'] -> get more similar images of this one