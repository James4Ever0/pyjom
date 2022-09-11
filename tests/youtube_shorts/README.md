turned out youtube shorts are searchable, downloadable.

but the video feed is not yet acquired, just like all other video feeds from youtube, twitch, reddit, qq小世界, bilibili, 抖音, tiktok and the trending ones.

the youtube advanced filter is embedded in the search results. you can only jump to one embedded link at a time

to get the next page on youtube:

the key seems to be the unified unlimited api key for youtube.

POST https://www.youtube.com/youtubei/v1/search?key=AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8&prettyPrint=false with a lot of headaching parameters.

you can bypass them. here are some basic parameters without lots of combinations. if you want to combine them, better figure it out yourself.

https://github.com/alexmercerind/youtube-search-python/blob/fc12c05747f1f7bd89d71699403762b86b523da5/youtubesearchpython/core/constants.py#L45