from pyjom.main import *
from typing import Generator


class OnlineAutoContentProducer(ContentProducer):
    def __init__(
        self,
        source=None,
        enable_log=True,
        fast: bool = True,
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
    ):  # something in this metaTopic is not droppable.
        super().__init__()
        assert source is not None
        self.source = source
        self.tempdir = tempdir
        self.fast = fast
        self.metaTopic = metaTopic  # 所谓的超话 超级话题
        if enable_log:
            self.log_location = "logs/local/"
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
                    OnlineProcessor, source=source
                ),  # this is the second thing. how do you process this?
                # "reviewer": filesystemReviewer,
                "producer": keywordDecorator(
                    OnlineProducer,  # what does this 'OnlineProducer' generate?
                    source=source,
                    template=template,
                    fast=self.fast,
                    template_configs=template_configs,
                ),
                "poster": keywordDecorator(
                    OnlinePoster, # you need to be prudent. this is not kids stuff. figure out how to post to multiple 
                    iterate=True,
                    contentType=contentType,
                    postMetadataGenerator=postMetadataGenerator,
                    platform=platform,
                )  # just for debugging.
                # you also need to change the logic below, for other 'dummy' stuffs.
                # 'poster':keywordDecorator(dummyPoster, iterate=True) # just for debugging.
            }
        )
