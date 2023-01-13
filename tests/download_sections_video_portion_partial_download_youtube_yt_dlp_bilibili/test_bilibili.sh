URL="https://www.bilibili.com/video/BV1Fs411k7e9" #老戴 马克思佩恩 分p视频
# 也可以直接网页parse

# URL="https://www.bilibili.com/video/BV1Cg411E7NF" #苏打baka 魔改机箱 合集
# 合集视频 用bilibili_api 或者直接网页parse即可

# it has multiple videos. what to do?
# --force-keyframes-at-cuts
# man i just need the first chapter.

# yt-dlp --download-sections "*0:05:00-0:06:30" --playlist-items "1" "$URL" # only first video.

# premium?
# Use --cookies-from-browser or --cookies for the authentication. See  https://github.com/yt-dlp/yt-dlp/wiki/FAQ#how-do-i-pass-cookies-to-yt-dlp 
# yt-dlp --download-sections "*0:05:00-0:06:30" --playlist-items "1" "$URL" # pass cookies.

# just want metadata?
# if you want title for each video in playlist, you just get it from elsewhere or parse the damn output filename (slow, man!)

# this seems to only have video description. nothing else! not even video length.
# yt-dlp --write-description --write-playlist-metafiles --skip-download "$URL"

# hey i don't want many download links. i just want title.
# yt-dlp --write-info-json  --write-playlist-metafiles --skip-download "$URL" # this will get metadata main playlist and every video in the playlist in separate json files.
# this is one of the video in that playlist. "https://www.bilibili.com/video/BV1Fs411k7e9?p=1

# you can get comments with this tool.
## no comments?
# yt-dlp --write-info-json --skip-download "$URL"
# download-sections can be used multiple times?