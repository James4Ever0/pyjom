from pyjom.commons import *
from pyjom.platforms.bilibili.uploader import uploadVideo
from typing import Generator
@decorator
def BilibiliPoster(content, iterate=False, postMetadataGenerator:=None # must be a generator. a called generator function.
,contentType='video', dedeuserid:str = "397424026"):
    # are you sure this 'postMetadataGenerator' will generate valid data for us?
    # anyway let's write for video.
    # there are two generators. what do you want?
    # def postContent(elem):
        print("READY TO POST CONTENT FROM:", elem)
    for postMedadata in postMetadataGenerator:
    if iterate:
        for elem in content:
    # content id?
    return "bilibili://{}/{}/{}".format(dedeuserid, contentType, contentId)
