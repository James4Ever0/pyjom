turned out youtube shorts are searchable, downloadable.

but the video feed is not yet acquired, just like all other video feeds from youtube, twitch, reddit, qq小世界, bilibili, 抖音, tiktok and the trending ones.

the youtube advanced filter is embedded in the search results. you can only jump to one embedded link at a time

to get the next page on youtube:

the key seems to be the unified unlimited api key for youtube.

POST https://www.youtube.com/youtubei/v1/search?key=AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8&prettyPrint=false with a lot of headaching parameters.

you can bypass them. here are some basic parameters without lots of combinations. if you want to combine them, better figure it out yourself.

some of them might already fail to work.

https://github.com/alexmercerind/youtube-search-python/blob/fc12c05747f1f7bd89d71699403762b86b523da5/youtubesearchpython/core/constants.py#L45

bilibili search api is currently simple:

https://search.bilibili.com/video?keyword=%E6%B1%AA%E6%B1%AA&from_source=webtop_search&spm_id_from=333.1007&search_source=3&tids=219&order=dm&duration=2