from pyjom.main import *
from typing import Generator
from types import FunctionType


class OnlineAutoContentProducer(ContentProducer):
    def __init__(
        self,
        source=None,
        debug=False,
        enable_log=True,
        fast: bool = True,
        afterPosting: FunctionType = ...,
        postMetadataGenerator: Generator = ...,
        processor_filters={},
        producer_filters={},
        platform: str = "bilibili",
        template: str = "pets_with_music_online",
        template_configs: list = [],  # list or 'template_config' generator
        contentType: str = "video",  # for poster.
        tempdir: str = "/dev/shm/medialang/online",
        metaTopic={
            "static": [["dog", "cat", "puppy"], ["funny", "cute"]],
            "dynamic": [["samoyed", "husky", "teddy", "chiwawa"]],
        },
        dog_or_cat='dog',
    ):  # something in this metaTopic is not droppable.
        super().__init__()
        # do afterPosting before even start it.
        # now we might want to check our product before another test.
        try:
            afterPosting()
        except:
            pass
        assert source is not None
        self.source = source
        self.tempdir = tempdir
        self.fast = fast
        self.metaTopic = metaTopic  # 所谓的超话 超级话题
        if enable_log:
            self.log_location = "logs/local/"  # what location?
        self.identifier.typeFix(type(self).__name__)
        self.methodsList.update(
            {
                "topic": keywordDecorator(
                    OnlineTopicGenerator, source=source, metaTopic=metaTopic
                ),  # how to generate this?
                "info": keywordDecorator(
                    OnlineFetcher, source=source, tempdir=tempdir
                ),  # can you do that?
                "processor": keywordDecorator(
                    OnlineProcessor, source=source, dog_or_cat=dog_or_cat
                ),  # this is the second thing. how do you process this?
                # "reviewer": filesystemReviewer,
                "producer": keywordDecorator(
                    OnlineProducer,  # what does this 'OnlineProducer' generate?
                    source=source,
                    template=template,
                    fast=self.fast,
                    template_configs=template_configs,
                    debug=debug,  # overkill?
                ),
                "poster": keywordDecorator(
                    OnlinePoster,  # you need to be prudent. this is not kids stuff. figure out how to post to multiple platforms the same time, figure out how to post to individual platform one by one.
                    iterate=True,
                    contentType=contentType,
                    postMetadataGenerator=postMetadataGenerator,
                    platform=platform,
                    afterPosting=afterPosting,
                )  # just for debugging.
                # you also need to change the logic below, for other 'dummy' stuffs.
                # 'poster':keywordDecorator(dummyPoster, iterate=True) # just for debugging.
            }
        )
