from pyjom.commons import *
from pyjom.platforms.bilibili.uploader import uploadVideo

@decorator
def BilibiliPoster(content, iterate=False, postMetadataGenerator=None,contentType='video'):
    # are you sure this 'postMetadataGenerator' will generate valid data for us?
    # anyway let's write for video.
    # there are two generators. what do you want?
    # def postContent(elem):
        print("READY TO POST CONTENT FROM:", elem)
    
    if iterate:
        for elem in content:
    # content id?
    return "bilibili://{}/{}/{}".format(dedeuserid, contentType, contentId)
