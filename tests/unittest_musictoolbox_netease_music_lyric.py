from test_commons import *
from pyjom.musictoolbox import neteaseMusic

NMClient = neteaseMusic()
# import random
query = "linkin park numb"
for sim in [False, True]:
    result = NMClient.getMusicAndLyricWithKeywords(query, similar=sim)
    print('similar?', sim)
    # no lyrics! wtf??
    breakpoint()