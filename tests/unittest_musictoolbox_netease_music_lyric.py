from test_commons import *
from pyjom.musictoolbox import neteaseMusic

NMClient = neteaseMusic()
# import random
query = "linkin park numb"
for sim in [False, True]:
    result = NMClient.getMusicAndLyricWithKeywords(query, similar=sim, debug=True)
    print("similar?", sim)
    # no lyrics! wtf??
    breakpoint()
# now let's test something surely will get lyrics.
# music_id = 497572729
# lyric_string = NMClient.getMusicLyricFromNetease(music_id)
# print("LYRIC STRING:",lyric_string)
# in case we don't get the lyric, you should be prepared.
# it works.
