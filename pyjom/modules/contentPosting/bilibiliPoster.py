from pyjom.commons import *
from pyjom.platforms.bilibili.uploader import uploadVideo
from typing import Generator
from lazero.filesystem.temp import tmpdir, getRandomFileNameUnderDirectoryWithExtension, tmpfile
# that generator you must put beforehand.
import cv2
@decorator
def BilibiliPoster(content, iterate=False, postMetadataGenerator:Generator=...,# must be a generator. a called generator function.
contentType='video', dedeuserid:str = "397424026", tempdir = '/dev/shm/medialang/bilibiliPoster'):
    # are you sure this 'postMetadataGenerator' will generate valid data for us?
    # anyway let's write for video.
    # there are two generators. what do you want?
    getPostMetadata = lambda: postMetadataGenerator.__next__()
    def postContent(elem): # what is this elem? please check for video producer.
        with tmpdir(path=tempdir):
        postMetadata = getPostMetadata()
        print("READY TO POST CONTENT FROM:", elem)# this elem is video location for me.
        if contentType == 'video': # single video upload without grouping.
            videoPath = elem
            cover_path = getRandomFileNameUnderDirectoryWithExtension('png',tempdir)
            cover_target, mTagSeries, mTitle, mBgm, mDescription, dog_or_cat_original, search_tid = postMetadata # assumptions on video type.
            with tmpfile(cover_path):
                cv2.imwrite(cover_path, cover_target)
            # you need to save this 'cover_target' to file.
                contentId = uploadVideo(dedeuserid = dedeuserid,description = mDescription,dynamic=mDescription, tagString = tarString)
        return "bilibili://{}/{}/{}".format(dedeuserid, contentType, contentId)
    
    def postContentIterate(content):
        for elem in content:
            yield postContent(elem)
    if iterate:
        return postContentIterate(content)
    else:
        return postContent(content)
    # content id?
