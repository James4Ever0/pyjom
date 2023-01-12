# actually the clip model does well for this.
# though you want to use bm25 based textrank

image = "prettyGirl.jpeg" # girl image

from PicImageSearch.sync import BaiDu

baidu = BaiDu()
result = baidu.search(file=image)
# print(result)
# better not to query 'ajax' unless you want to get banned.
# breakpoint()
# you want to use phash, width, height for this.
import requests
SLEEP= 1
for elem in result.raw:
    elem = elem.__dict__
    # print(elem)
    # breakpoint()
    thumbnail = elem.get('thumbnail')
    simi = elem.get('similarity')
    title = elem.get('title')
    # url is not necessary since we almost can't get the picture.
    ajaxUrl = elem['origin'].get('ajaxUrl')
    import time
    print(thumbnail, simi, title)
    # print(thumbnail, simi, title, ajaxUrl)
    time.sleep(SLEEP) # wait too long?
    r = requests.get(ajaxUrl)
    myJson = r.json()
    # from lazero.filesystem.io import writeJsonObjectToFile
    # writeJsonObjectToFile('jq_image_2.json',myJson)
    # breakpoint()
    # maybe no need to parse this thing.

    # try: # TODO: skipping this parsing since multiple errors.
    #     from parse_baidu_search_ajax import getBaiduImageSearchAjaxInfoParsed
    #     title_some, url_meta_some= getBaiduImageSearchAjaxInfoParsed(myJson, debug=True)
    #     # changed again?
    # except:
    #     import traceback
    #     traceback.print_exc()
    #     print(ajaxUrl)
    #     print('error!')
    #     breakpoint()

    # breakpoint()
# ['origin', 'raw', 'url']
# result.raw[0].url is the original url. however you won't get the picture.
# result.raw[0].thumbnail
# 'origin', 'similarity', 'thumbnail', 'title', 'url'
# result.raw[0].origin['ajaxUrl'] -> get more similar images of this one