import os
commands = ["pip3 install yt-dlp",'yt-dlp --write-subs --convert-subtitles srt "https://m.youtube.com/watch?v=At7ORzmAaT4"'] # get recommendation this time.

# we will still get many videoId from curl.


for c in commands:
    os.system(c)