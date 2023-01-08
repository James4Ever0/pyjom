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
import requests


def registerBilibiliUserVideo(
    bvid: str,
    dedeuserid: str,
    is_mine: bool = True,
    visible: bool = False,
    server_domain: str = "localhost",
    server_endpoint: str = "registerUserVideo",
    server_port: int = 7341,
    success_codes: list[int] = [200, 201],
):
    data = {
        "bvid": bvid,
        "dedeuserid": dedeuserid,
        "is_mine": is_mine,
        "visible": visible,
    }

    r = requests.post(
        "http://{}:{}/{}".format(server_domain, server_port, server_endpoint), json=data
    )
    register_success = r.status_code in success_codes
    return register_success


# why you have decorator? so OnlinePoster will not have decorator.
@decorator
def BilibiliPoster(
    content,
    iterate=False,
    getPostMetadata=...,  # some lambda calling generator.__next__()
    contentType="video",
    dedeuserid: str = "397424026",
    tempdir="/dev/shm/medialang/bilibiliPoster",
    afterPosting: FunctionType = ...,
):
    # are you sure this 'postMetadataGenerator' will generate valid data for us?
    # anyway let's write for video.
    # there are two generators. what do you want?
    # getPostMetadata = lambda: postMetadataGenerator.__next__()
    from retry import retry

    @retry(tries=3, delay=5)  # if causing trouble
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
            afterPosting()  # execute no matter what. after posting the content.
            # now register the uploaded video.
            if contentType == "video":
                video_bvid = (
                        contentId
                        if type(contentId) == str
                        else contentId.get("bvid", contentId.get("BVID"))
                    )
                register_success = registerBilibiliUserVideo(
                    video_bvid,
                    str(dedeuserid),
                )
                print("VIDEO REGISTRATION STATUS?", register_success)
                if not register_success:
                    print("VIDEO REGISTRATION ERROR")
                    breakpoint()
            if type(contentId) == str:
                video_identifier = "bvid_{}".format(contentId)
            else:
                video_identifier = "aid_{}_bvid_{}".format(
                    contentId.get("aid"), contentId.get("bvid")
                )
            return "bilibili://{}/{}/{}".format(
                dedeuserid, contentType, video_identifier
            )  # this content id is fucked.

    def postContentIterate(content):
        for elem in content:
            yield postContent(elem)

    if iterate:
        return postContentIterate(content)
    else:
        return postContent(content)
    # content id?
