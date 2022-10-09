from pyjom.commons import *
from pyjom.platforms.bilibili.uploader import uploadVideo
from typing import Generator

# that generator you must put beforehand.
@decorator
def BilibiliPoster(content, iterate=False, postMetadataGenerator:Generator=...,# must be a generator. a called generator function.
contentType='video', dedeuserid:str = "397424026"):
    # are you sure this 'postMetadataGenerator' will generate valid data for us?
    # anyway let's write for video.
    # there are two generators. what do you want?
    getPostMetadata = lambda: postMetadataGenerator.__next__()
    def postContent(elem,):
        postMetadata = getPostMetadata()
        print("READY TO POST CONTENT FROM:", elem)
        return "bilibili://{}/{}/{}".format(dedeuserid, contentType, contentId)
    
    def postContentIterate(content):
        for elem in content:
            yield postContent(elem)
    if iterate:
        return postContentIterate(content)
    else:
        return postContent(content)
    # content id?
