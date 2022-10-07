import os
commands = ["pip3 install yt-dlp",'yt-dlp --write-subs --convert-subtitles srt  "https://m.youtube.com/watch?v=At7ORzmAaT4"']
# commands = ["pip3 install yt-dlp",'yt-dlp --write-subs --convert-subtitles srt --sponsorblock-mark poi_highlight "https://m.youtube.com/watch?v=At7ORzmAaT4"']

# this will mark the highlights.

for c in commands:
    os.system(c)