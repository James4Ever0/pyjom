URL="https://www.bilibili.com/video/BV1Fs411k7e9" #老戴 马克思佩恩
#
# it has multiple videos. what to do?
# --force-keyframes-at-cuts
# man i just need the first chapter.
yt-dlp --download-sections "*0:05:00-0:06:30" "$URL"
# download-sections can be used multiple times?