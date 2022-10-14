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
    elem = elem.__dict__
    print(elem)
    breakpoint()
    thumbnail = elem.get('thumbnail')
    simi = elem.get('similarity')
    title = elem.get('title')
    # url is not necessary since we almost can't get the picture.
    ajaxUrl = elem['origin'].get('ajaxUrl')
    print(thumbnail, simi, title, ajaxUrl)
# ['origin', 'raw', 'url']
# result.raw[0].url is the original url. however you won't get the picture.
# result.raw[0].thumbnail
# 'origin', 'similarity', 'thumbnail', 'title', 'url'
# result.raw[0].origin['ajaxUrl'] -> get more similar images of this one