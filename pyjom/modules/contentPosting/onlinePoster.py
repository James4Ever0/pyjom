from email.generator import Generator
from pyjom.modules.contentPosting.bilibiliPoster import BilibiliPoster


def OnlinePoster(
    content,
    iterate=False,
    contentType="video",
    postMetadataGenerator: Generator = ...,
    platform="bilibili",
):
    posters = {"bilibili": BilibiliPoster}
    assert platform in posters.keys()
    return posters[platform](
        content,
        iterate=iterate,
        contentType=contentType,
        getPostMetadata=getPostMetadata,
    )
