from pyjom.commons import *
from pyjom.platforms.bilibili.uploader import 

@decorator
def BilibiliPoster(content, iterate=False, contentType='video'):
    if iterate:
        for elem in content:
            print("READY TO POST CONTENT FROM:", elem)
    # content id?
    return "bilibili://{}/{}/{}".format(dedeuserid, contentType, contentId)
