from pyjom.commons import *


@decorator
def BilibiliPoster(content, iterate=False, contentType='video'):
    if iterate:
        for elem in content:
            print("READY TO POST CONTENT FROM:", elem)
    return "bilibili://{}/{}/{}".format(dedeuserid, contentType, contentId)
