# check if is the video we want and extract data or discard.

# let's just view here:
# https://github.com/SocialSisterYi/bilibili-API-collect

videoLinks = [
    "https://www.bilibili.com/video/BV1e54y1y7qy",  # 女攻男受 emm
    "https://www.bilibili.com/video/BV1P441197oV",  # in which you shall never find anything interesting.
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
    # r = requests.get("https://api.bilibili.com/x/web-interface/view?bvid=BV1e54y1y7qy")
    r.raise_for_status()
    r_tags.raise_for_status()
    # "need_jump_bv":false
    # bvid only?

    response_json = r.json()
    response_tags_json = r_tags.json()
    # it must be json.
    import rich
    rich.print(response_json)
    assert response_json['code'] == 0
    assert response_tags_json['code'] == 0

    data = response_json['data']
    tags_data = response_tags_json['data']

    title = data['title']
    pic = data['pic']
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
    page_count = len(pages)
    for page in pages:
        page_name = page['part']
        page_dimension = page['dimension']
        page_duration = 

    breakpoint()