# check if is the video we want and extract data or discard.

# we name downloaded video using some agreements.
import os
videoID="BV1e54y1y7qy"
url = f"https://www.bilibili.com/video/{videoID}" # only one single page.
# 290 seconds.
# section example:
# 0:05:00-0:06:30
cmd=f'yt-dlp --download-sections "*{start}-{end}" --playlist-items "1"'

os.system(cmd)