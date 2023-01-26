# get video metadata first. we may filter unwanted videos by metadata.

# let's just view here:
# https://github.com/SocialSisterYi/bilibili-API-collect

# i found new format of video shortlink:
# https://b23.tv/BV1zW4y1p7RT
# https://b23.tv/<bvid>

videoLinks = [
    "https://www.bilibili.com/video/BV1e54y1y7qy",  # 女攻男受 emm
    "https://www.bilibili.com/video/BV1P441197oV",  # in which you shall never find anything interesting. no related video.
    "https://www.bilibili.com/video/BV1Fs411k7e9", # multiple chapters, you shall not find this interesting.
    "https://www.bilibili.com/video/av5842509" # aid version of video link.
]
# import fake_useragent
# ua = fake_useragent.UserAgent()
import re
from pymaybe import maybe
import requests
from urllib.parse import urlencode

def extractBVID(chars:str):
    bvid = maybe(re.findall(r"/(BV[a-zA-Z0-9]+)",chars))[0]
    return bvid

def extractAID(chars:str):
    aid = maybe(re.findall(r"/av([0-9]+)",chars))[0]
    return aid

## remember the video is always scrapable via av id.
## av5842509

# https://api.bilibili.com/x/web-interface/view?aid=<AID>
# https://api.bilibili.com/x/web-interface/view?bvid=<BVID>

# videoDownloadPath = ""

# shit!

# why i need to download whole damn video? i need to cut it into bite-sized video!

# for some video there's no possibility to determine the source.
# let's see the video metadata.

# import os

# os.system(f'yt-dlp --dump-metadata --output metadata.json "{videoLinks[0]}"') # working?

# bullshit. we shall get the video metadata first.
url = "https://api.bilibili.com/x/web-interface/view"
tags_url = "https://api.bilibili.com/x/tag/archive/tags"
related_url = "https://api.bilibili.com/x/web-interface/archive/related"

for videoLink in videoLinks:
    bvid = extractBVID(videoLink)
    if bvid:
        params = {"bvid": bvid}
    else:
        aid = extractAID(videoLink)
        if aid:
            params = {"aid": aid}
        else:
            print("no valid bilibili video id found.")
            print("skipping video link:", videoLink)
            continue
    
    # print("PARAMS?",params)
    # shit.
    r = requests.get(f"{url}?{urlencode(params)}") # why? what the fuck?
    r_tags = requests.get(f"{tags_url}?{urlencode(params)}")
    # r = requests.get(url,data=params,headers={"User-Agent":ua.random})
    r_related = requests.get(f'{related_url}?{urlencode(params)}')
    # r = requests.get("https://api.bilibili.com/x/web-interface/view?bvid=BV1e54y1y7qy")
    r.raise_for_status()
    r_tags.raise_for_status()
    r_related.raise_for_status()
    # "need_jump_bv":false
    # bvid only?

    response_json = r.json()
    response_tags_json = r_tags.json()
    response_related_json = r_related.json()
    # it must be json.
    import rich
    # rich.print(response_json)
    assert response_json['code'] == 0
    assert response_tags_json['code'] == 0
    assert response_related_json['code'] == 0

    data = response_json['data']
    tags_data = response_tags_json['data']
    related_data = response_related_json['data']

    ## parsing video stats.

    title = data['title']
    pic = data['pic']
    tid,tname = data['tid'],data['tname']
    # 27, "综合"
    # 253, "动漫杂谈"
    dynamic = data['dynamic'] # we can copy that.
    desc = data['desc']
    owner_mid = data['owner']['mid']

    state = data['state']
    assert state == 0 # make sure this video is downloadable.

    stat =  data['stat']

    view  = stat['view']
    reply = stat['reply']
    danmaku = stat['danmaku']
    favorite = stat['favorite']
    coin  = stat['coin']
    share = stat['share']
    like  = stat['like']


    pages = data['pages']
    page_count = len(pages) # data['videos']
    for page in pages:
        page_index = page['page']
        page_name = page['part']
        page_dimension = page['dimension']
        page_width, page_height, page_rotate = page_dimension['width'], page_dimension['height'], page_dimension['rotate']
        page_duration = page['duration']
    
    # subtitle = data['subtitle']
    # let's just skip.

    ## parsing tags info.
    for tag in tags_data:
        tag_id = tag['tag_id']
        tag_name = tag['tag_name']
        tag_used = tag['count']['use']
        tag_attention = tag['count']['atten']
        # introduction of tag.
        tag_content = tag['content']
        tag_short_content = tag['short_content']
    
    ## extract related video info.
    related_video_counts = len(related_data)
    for related_video in related_data:
        related_aid = related_video['aid']
        related_bvid = related_video['bvid']

        related_tid = related_video['tid']
        related_tname = related_video['tname']
        related_pic = related_video['pic']
        related_title = related_video['title']
        related_page_count = related_video['videos'] # make sure this is 1?
        related_desc = related_video['desc']
        related_state = related_video['state']
        if related_state != 0: continue
        related_duration = related_video['duration']
        related_owner_mid = related_video['owner']['mid']
        related_stat = related_video['stat']
        related_dynamic = related_video['dynamic']
        # well, we've got non-standard dimensions.
        related_dimension = related_video['dimension']
        # no tag here? you might want more!
    breakpoint()