from pyjom.main import *


class OnlineAutoContentProducer(ContentProducer):
    def __init__(
        self,
        source=None,
        enable_log=True,
        processor_filters={},
        producer_filters={},
        template="pets_with_music_online",
        template_config={},
        tempdir
        metaTopic={
            "static": [["dog", "cat", 'puppy'], ["funny", "cute"]],
            "dynamic": [["samoyed", "husky", "teddy", "chiwawa"]],
        },
    ):  # something in this metaTopic is not droppable.
        super().__init__()
        assert source is not None
        self.source = source
        self.tempdir = tempdir
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
                    OnlineFetcher, source=source, tempdir = tempdir
                ),  # can you do that?
                "processor": keywordDecorator(
                    OnlineProcessor, filters=processor_filters
                ),  # this is the second thing. how do you process this?
                # "reviewer": filesystemReviewer,
                "producer": keywordDecorator(
                    OnlineProducer,
                    filters=producer_filters,
                    template=template,
                    template_config=template_config,
                ),
            }
        )
