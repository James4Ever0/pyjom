# check if is the video we want and extract data or discard.

videoLinks = [
    "https://www.bilibili.com/video/BV1e54y1y7qy",  # 女攻男受 emm
    "https://www.bilibili.com/video/BV1P441197oV",  # in which you shall never find anything interesting.
    "https://www.bilibili.com/video/BV1Fs411k7e9", # multiple chapters, you shall not find this interesting.
]

## remember the video is always scrapable via av id.
## av5842509

https://api.bilibili.com/x/web-interface/view?aid=<AID>
https://api.bilibili.com/x/web-interface/view?bvid=<BVID>

# videoDownloadPath = ""

# shit!

# why i need to download whole damn video? i need to cut it into bite-sized video!

# for some video there's no possibility to determine the source.
# let's see the video metadata.

# import os

# os.system(f'yt-dlp --dump-metadata --output metadata.json "{videoLinks[0]}"') # working?

# bullshit. we shall get the video metadata first.
