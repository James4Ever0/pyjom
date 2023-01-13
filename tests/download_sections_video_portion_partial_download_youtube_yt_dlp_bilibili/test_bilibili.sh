# 关于视频合集 分p视频的分析逻辑：
# https://github.com/Satoing/python_bilibili_downloader/blob/master/bilibili_video.py

# 解析这个接口可以得到分p或者合集的信息 以及字幕信息 AI生成的字幕
# https://api.bilibili.com/x/web-interface/view?bvid=BV1Fs411k7e9
# https://api.bilibili.com/x/web-interface/view?bvid=BV1Cg411E7NF

URL="https://www.bilibili.com/video/BV1Fs411k7e9" #老戴 马克思佩恩 分p视频
# 也可以直接网页parse

# executing this you will get "subtitle" in "danmaku" as language, in xml format.
# 对于海量弹幕的某些视频 （超电磁炮 12w asoul的某些二创 3w）不建议进行弹幕分析 可以通过API获取弹幕总数 不下载弹幕 
# yt-dlp --skip-download --list-subs -I 1 "https://www.bilibili.com/video/BV1Fs411k7e9"

# URL="https://www.bilibili.com/video/BV1Cg411E7NF" #苏打baka 魔改机箱 合集
# 合集视频 用bilibili_api 或者直接网页parse即可

# it has multiple videos. what to do?
# --force-keyframes-at-cuts
# man i just need the first chapter.

# yt-dlp --download-sections "*0:05:00-0:06:30" --playlist-items "1" "$URL" # only first video.

# premium?
# this feature is awesome! how to extract cookies programmatically from browser?
# Use --cookies-from-browser or --cookies for the authentication. See  https://github.com/yt-dlp/yt-dlp/wiki/FAQ#how-do-i-pass-cookies-to-yt-dlp 

# not working for chromium on kali? (no bilibili cookie found) maybe it is relocated.
# cookies = yt_dlp.cookies.extract_cookies_from_browser(BROWSER_NAME) -> YourubeDLCookieJar

# save as Netscape HTTP Cookie File.
# cookies.save(OUTPUT_FILE_PATH) 

# since we have issue playing content at tail of video, we do this.
# yt-dlp --download-sections "*0:05:00-0:06:30" --playlist-items "1" --cookies-from-browser firefox --force-keyframes-at-cuts "$URL" # pass cookies.

# forcing keyframe is much slower. but it produces better results.
# yt-dlp --download-sections "*0:05:00-0:06:30" --playlist-items "1" --cookies-from-browser firefox --force-keyframes-at-cuts "$URL" # pass cookies.

# you may want to add some margin at tail (or head) if not using "--force-keyframes-at-cuts", be it 10 seconds. usually jigs happens at 5 secs. but we are careful.

# yt-dlp --download-sections "*0:04:50-0:06:40" --playlist-items "1" --cookies-from-browser firefox "$URL" # pass cookies.

# what if we download multiple sections?

# no combination? shit.

# if not at the very tail, other tails can be better than the last tail. but it is just my guess. better to keep all these margins!

# yt-dlp --download-sections "*0:04:50-0:05:40" --download-sections "*0:05:50-0:06:40" --playlist-items "1" --cookies-from-browser firefox -o "%(uploader_id)s-%(id)s-%(title)s-%(autonumber)s.%(ext)s" "$URL" # pass cookies.

# since we have cron job now, no need to do the old-school thing.
yt-dlp --download-sections "*0:04:50-0:05:40" --download-sections "*0:05:50-0:06:40" --playlist-items "1" --cookies /root/.browser_cookies_exported/firefox.cookies -o "%(uploader_id)s-%(id)s-%(title)s-%(autonumber)s.%(ext)s" "$URL" # pass cookies in different way

# like this: '2142762-BV1Fs411k7e9_p1-老戴《马克思佩恩 3》全收集流程攻略【共14期完结】 p01 EP-01-00002.mp4'
# https://github.com/yt-dlp/yt-dlp#readme -> "OUTPUT TEMPLATE"
# https://github.com/yt-dlp/yt-dlp/issues/4579

# you better use stored cookies instead of retrieving cookies every time.
# or you can update cookies regularly with cronjob.

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