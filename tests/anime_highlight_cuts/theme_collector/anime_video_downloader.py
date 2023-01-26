# we name downloaded video using some agreements.
import os

videoIDs = [
    "BV1e54y1y7qy",  # 842224692_part1-00001
    "BV1Qf4y197bt",  # great challange, 286760784
    "BV1bi4y1g7Gd",  # watermark, full screen, 541755429
    "BV1PA411n7N6",  # shit jumping around, 329297394
]

videoID = videoIDs[3]
from bv2av import bv_av_conversion

videoIDAlternative = bv_av_conversion(videoID)

if videoIDAlternative is None: # not av or bv. shit happened!
    raise Exception("")

import re

print(videoAVID, type(videoAVID))
videoAID = re.findall(r"\d+", videoAVID)[0]

url = f"https://www.bilibili.com/video/{videoBVID}"  # only one single page.
# 290 seconds.
# section example:
# 0:05:00-0:06:30
# import time
# secondsToHHMMSS = lambda seconds:time.strftime('%H:%M:%S', time.gmtime(seconds))

# some formats are not working. fuck.

playlistIndex = "1"

# start = secondsToHHMMSS(100)
# end = secondsToHHMMSS(150)

# print('TIMESPAN:',start, end)

nameFormat = "%(id)s-%(autonumber)s.%(ext)s"
cmd = f'yt-dlp --playlist-items "{playlistIndex}" -o "{nameFormat}" "{url}"'
# cmd=f'yt-dlp --download-sections "*{start}-{end}" --playlist-items "{playlistIndex}" -o "{nameFormat}"  "{url}"'

os.system(cmd)
autonumber = "1".zfill(5)
expectedNamePrefix = f"{videoAID}_part{playlistIndex}-{autonumber}"
print("expected filename prefix:", expectedNamePrefix)
files = os.listdir(".")

for fname in files:
    if fname.startswith(expectedNamePrefix):
        print("TARGET FOUND!")
        print("FILENAME:", fname)
