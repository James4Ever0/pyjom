# URL="https://www.bilibili.com/video/BV1Fs411k7e9" #老戴 马克思佩恩 分p视频
#

# URL="https://www.bilibili.com/video/BV1Cg411E7NF" #苏打baka m

# it has multiple videos. what to do?
# --force-keyframes-at-cuts
# man i just need the first chapter.

# yt-dlp --download-sections "*0:05:00-0:06:30" --playlist-items "1" "$URL" # only first video.

# just want metadata?
# yt-dlp --write-info-json  --write-playlist-metafiles --skip-download "$URL" # this will get metadata main playlist and every video in the playlist in separate json files.
# this is one of the video in that playlist. "https://www.bilibili.com/video/BV1Fs411k7e9?p=1

# you can get comments with this tool.
## no comments?
yt-dlp --write-info-json --skip-download "$URL"
# download-sections can be used multiple times?