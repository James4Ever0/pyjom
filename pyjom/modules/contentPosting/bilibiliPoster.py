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
    def postContent(elem): # what is this elem? please check for video producer.
        postMetadata = getPostMetadata()
        print("READY TO POST CONTENT FROM:", elem)# this elem is video location for me.
        if contentType == 'video': # single video upload without grouping.
            videoPath = elem
            # you need to save this 'cover_target' to path.
            cover_target, mTagSeries, mTitle, mBgm, mDescription, dog_or_cat_original, search_tid = postMetadata # assumptions on video type.
            contentId = uploadVideo(dedeuserid = dedeuserid,description = )
        return "bilibili://{}/{}/{}".format(dedeuserid, contentType, contentId)
    
    def postContentIterate(content):
        for elem in content:
            yield postContent(elem)
    if iterate:
        return postContentIterate(content)
    else:
        return postContent(content)
    # content id?
