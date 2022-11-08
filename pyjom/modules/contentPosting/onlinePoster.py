from reloading import reloading
from types import FunctionType
from typing import Generator
from pyjom.modules.contentPosting.bilibiliPoster import BilibiliPoster

# there is no decorator!
@reloading
def OnlinePoster(
    content,
    iterate=False,
    contentType="video",
    postMetadataGenerator: Generator = ...,
    platform="bilibili",
    afterPosting:FunctionType=...
):
    posters = {"bilibili": BilibiliPoster}
    assert platform in posters.keys()
    getPostMetadata = lambda: postMetadataGenerator.__next__()
    return posters[platform](
        content,
        iterate=iterate,
        contentType=contentType,
        getPostMetadata=getPostMetadata,
        afterPosting=afterPosting,
    )
