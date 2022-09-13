from pyjom.main import *

class OnlineAutoContentProducer(ContentProducer):
    def __init__(self, source=None, enable_log=True,processor_filters={},producer_filters={}, path_replacers = [], template="pets_with_music_online", template_config = {}):
        super().__init__()
        assert source is not None
        self.source = source
        if enable_log:
            self.log_location = "logs/local/"
        self.identifier.typeFix(type(self).__name__)
        self.methodsList.update(
            {
                "topic":keywordDecorator(OnlineTopicGenerator, source=source),  # how to generate this?
                "info": keywordDecorator(OnlineFetcher, source=source), # can you do that?
                "processor": keywordDecorator(OnlineProcessor,reviewerLogs=self.reviewerLogs,filters=processor_filters, path_replacers = path_replacers), # this is the second thing. how do you process this?
                # "reviewer": filesystemReviewer,
                "producer": keywordDecorator(FilesystemProducer, filters=producer_filters, template=template,template_config = template_config),
            }
        )

    def get_one_topic(self):
        topic, source = self.methodsList["topic"](
            filepath=self.filepath, dirpath=self.dirpath, recursive=self.recursive
        )  # a sequence of things.
        self.identifier.topicFix(source)
        return topic
# ctrl + shift + t: reopen closed tab in vscode