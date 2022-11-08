from reloading import reloading
from types import FunctionType
from pyjom.commons import *
from pyjom.platforms.bilibili.uploader import uploadVideo

from lazero.filesystem.temp import (
    tmpdir,
    getRandomFileNameUnderDirectoryWithExtension,
    tmpfile,
)

# that generator you must put beforehand.
import cv2


# why you have decorator? so OnlinePoster will not have decorator.
@decorator
@reloading
def BilibiliPoster(
    content,
    iterate=False,
    getPostMetadata=...,  # some lambda calling generator.__next__()
    contentType="video",
    dedeuserid: str = "397424026",
    tempdir="/dev/shm/medialang/bilibiliPoster",
    afterPosting:FunctionType=...
):
    # are you sure this 'postMetadataGenerator' will generate valid data for us?
    # anyway let's write for video.
    # there are two generators. what do you want?
    # getPostMetadata = lambda: postMetadataGenerator.__next__()
    from retry import retry
    @retry(tries=3, delay=5) # if causing trouble
    def postContent(elem):  # what is this elem? please check for video producer.
        with tmpdir(path=tempdir):
            postMetadata = getPostMetadata()
            print(
                "READY TO POST CONTENT FROM:", elem
            )  # this elem is video location for me.
            if contentType == "video":  # single video upload without grouping.
                videoPath = elem
                cover_path = getRandomFileNameUnderDirectoryWithExtension(
                    "png", tempdir
                )
                (
                    cover_target,
                    mTagSeries,  # are you sure this is a list of tags?
                    mTitle,
                    mBgm,  # what is the bgm here used for?
                    mDescription,
                    dog_or_cat_original,  # what again is this dog/cat label?
                    search_tid,
                ) = postMetadata  # assumptions on video type.
                # you can fetch this from database. you can pickle this thing.
                tagString = ",".join(mTagSeries)
                # will have exceptions when having name clash. handle it!
                with tmpfile(cover_path):
                    cv2.imwrite(cover_path, cover_target)
                    # you need to save this 'cover_target' to file.
                    contentId = uploadVideo(
                        dedeuserid=dedeuserid,  # by decorator.
                        description=mDescription,
                        dynamic=mDescription,
                        tagString=tagString,
                        tagId=search_tid,
                        cover_path=cover_path,
                        videoPath=videoPath,
                        title=mTitle,
                    )  # choose to upload and get bvid.
            else:
                raise Exception(
                    "unknown content type to upload for bilibiliPoster:", contentType
                )
            afterPosting() # execute no matter what. after posting the content.
            return "bilibili://{}/{}/{}".format(dedeuserid, contentType, contentId)

    def postContentIterate(content):
        for elem in content:
            yield postContent(elem)

    if iterate:
        return postContentIterate(content)
    else:
        return postContent(content)
    # content id?
