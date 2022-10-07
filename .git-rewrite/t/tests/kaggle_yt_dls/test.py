import os
commands = ["pip3 install yt-dlp",'yt-dlp "https://m.youtube.com/watch?v=FuV63EEhS8c"']

for c in commands:
    os.system(c)