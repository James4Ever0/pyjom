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
playlistIndex='1'
start = secondsToHHMMSS(150)
end = secondsToHHMMSS(200)
nameFormat = "%(id)s-%(playlist_index)s-%(autonumber)s.%(ext)s"
cmd=f'yt-dlp --download-sections "*{start}-{end}" --playlist-items "{playlistIndex}" -o "{nameFormat}" "{url}"'

os.system(cmd)
autonumber = "1".zfill(5)
expectedNamePrefix = f"{videoID}-{playlistIndex}-{autonumber}"
print('expected filename prefix:', expectedNamePrefix)
files = os.listdir(".")
for fname in files:
    if fname.startswith(expectedNamePrefix):
        print("TARGET FOUND!")
        print("FILENAME:", fname)
