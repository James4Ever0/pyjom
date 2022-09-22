videoLink = ""

from lazero.filesystem.temp import tmpfile

import yt_dlp
# import pyidm
path = "./randomName.mp4"
x = yt_dlp.YoutubeDL({"outtmpl":path,'format':'[ext=mp4]'})
y = x.download([url])