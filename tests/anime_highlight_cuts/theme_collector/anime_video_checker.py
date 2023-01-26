# check if is the video we want and extract data or discard.

# we name downloaded video using some agreements.
import os
videoID="BV1e54y1y7qy"
url = f"https://www.bilibili.com/video/{videoID}" # only one single page.
# 290 seconds.
# section example:
# 0:05:00-0:06:30
import time
secondsToHHMMSS = lambda seconds:time.strftime('%H:%M:%S', time.gmtime(seconds))
items='1'
start = secondsToHHMMSS(150)
end = secondsToHHMMSS(200)
cmd=f'yt-dlp --download-sections "*{start}-{end}" --playlist-items "{items}" "{url}"'

os.system(cmd)