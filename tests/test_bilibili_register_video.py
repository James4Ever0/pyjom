dedeuserid = str(397424026)
bvid = "BV1Gd4y1j7ht"
from test_commons import *
from pyjom.modules.contentPosting.bilibiliPoster import registerBilibiliUserVideo

success = registerBilibiliUserVideo(bvid, dedeuserid)
print("SUCCESS?", success)
