from pyjom.main import *


class FilesystemContentReviewer(ContentReviewer):
    def __init__(self, filepath=None, dirpath=None, recursive=False, enable_log=True):
        super().__init__()
        if filepath is None:
            assert dirpath is not None
        else:
            raise Exception("filepath and dirpath cannot both be None.")
        self.filepath = filepath
        self.dirpath = dirpath
        self.recursive = recursive
        if enable_log:
            self.log_location = "logs/local/"
        self.identifier.typeFix(type(self).__name__)
        self.methodsList.update(
            {
                "topic": filesystemTopicGenerator,  # how to generate this?
                "fetcher": filesystemFetcher,
                "reviewer": filesystemReviewer,
            }
        )

    def get_one_topic(self):
        topic, source = self.methodsList["topic"](
            filepath=self.filepath, dirpath=self.dirpath, recursive=self.recursive
        )  # a sequence of things.
        self.identifier.topicFix(source)
        return topic


class FilesystemAutoContentReviewer(FilesystemContentReviewer):
    def __init__(
        self,
        filepath=None,
        dirpath=None,
        recursive=False,
        enable_log=True,
        semiauto=True,
        dummy_auto=True,
        template_names=[],
        args={},
    ):
        super().__init__(
            filepath=filepath,
            dirpath=dirpath,
            recursive=recursive,
            enable_log=enable_log,
        )
        self.identifier.typeFix(type(self).__name__)
        self.methodsList.update(
            {
                "reviewer": keywordDecorator(
                    filesystemReviewer,
                    auto=True,
                    semiauto=semiauto,
                    dummy_auto=dummy_auto,
                    template_names=template_names,
                    args=args,
                )
            }
        )

class FilesystemAutoContentProducer(ContentProducer):
    def __init__(self, filepath=None, dirpath=None, recursive=False, enable_log=True,reviewerLogs = [],processor_filters={},producer_filters={}, path_replacers = [], template="pets_with_music", template_config = {}):
        super().__init__()
        if filepath is None:
            assert dirpath is not None
        else:
            raise Exception("filepath and dirpath cannot both be None.")
        self.filepath = filepath
        self.dirpath = dirpath
        self.recursive = recursive
        self.reviewerLogs = reviewerLogs
        if enable_log:
            self.log_location = "logs/local/"
        self.identifier.typeFix(type(self).__name__)
        self.methodsList.update(
            {
                "topic": filesystemTopicGenerator,  # how to generate this?
                "info": filesystemFetcher, # can you do that?
                "processor": keywordDecorator(FilesystemProcessor,reviewerLogs=self.reviewerLogs,filters=processor_filters, path_replacers = path_replacers), # this is the second thing. how do you process this?
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