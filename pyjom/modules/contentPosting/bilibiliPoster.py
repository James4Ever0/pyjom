from pyjom.commons import *
from pyjom.platforms.bilibili.uploader import uploadVideo

@decorator
def BilibiliPoster(content, iterate=False, postMetadataGenerator=None,contentType='video'):
    # are you sure this 'postMetadataGenerator' will generate valid data for us?
    if iterate:
        for elem in content:
            print("READY TO POST CONTENT FROM:", elem)
    # content id?
    return "bilibili://{}/{}/{}".format(dedeuserid, contentType, contentId)
