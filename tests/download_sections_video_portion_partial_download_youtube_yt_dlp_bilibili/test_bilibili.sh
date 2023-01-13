URL="https://www.bilibili.com/video/BV1Fs411k7e9"
# --force-keyframes-at-cuts
yt-dlp --download-sections "*0:05:00-0:06:30" "$URL"
# download-sections can be used multiple times?