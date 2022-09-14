from pyjom.main import *

class OnlineAutoContentProducer(ContentProducer):
    def __init__(self, source=None, enable_log=True,processor_filters={},producer_filters={}, template="pets_with_music_online", template_config = {}, metaTopic=[["samoyed", "dog", "cat"], ["funny", "cute"]]):
        super().__init__()
        assert source is not None
        self.source = source
        self.metaTopic = metaTopic # 所谓的"超话
        if enable_log:
            self.log_location = "logs/local/"
        self.identifier.typeFix(type(self).__name__)
        self.methodsList.update(
            {
                "topic":keywordDecorator(OnlineTopicGenerator, source=source, topic=topic),  # how to generate this?
                "info": keywordDecorator(OnlineFetcher, source=source), # can you do that?
                "processor": keywordDecorator(OnlineProcessor,filters=processor_filters), # this is the second thing. how do you process this?
                # "reviewer": filesystemReviewer,
                "producer": keywordDecorator(OnlineProducer, filters=producer_filters, template=template,template_config = template_config),
            }
        )