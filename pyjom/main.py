from types import GeneratorType
from pyjom.commons import *  # really swap this shit?
from pyjom.modules import *


class ContentProducer:
    def __init__(self):
        self.uuid = dummyId()
        self.log_location = None
        self.trash_location = None
        self.methodsList = {
            "topic": dummyTopic,
            "info": dummyInfo,
            "processor": dummyProcessor,
            "producer": dummyProducer,
            "poster": dummyPoster,
            # below three all switched to 'auto' mode for iterating generators.
            "feedback": dummyFeedback,
            "optimizer": dummyOptimizer,
            "updator": dummyUpdator,
            "identifier": dummyIdentifier,
        }
        self.identifier = self.get_one_identifier(
            self.uuid
        )  # make sure occasionly used methods can be regenerated.
        self.identifier.typeFix(type(self).__name__)

    def get_one_identifier(self, uuid):
        return self.methodsList["identifier"](uuid)

    def get_one_topic(self):
        topic, source = self.methodsList["topic"]()
        self.identifier.topicFix(source)
        return topic

    def get_some_info(self, topic):
        info, source = self.methodsList["info"](topic)
        self.identifier.infoFix(source)
        return info

    def process_some_info(self, info):
        method = self.methodsList["processor"]
        # print(method)
        # breakpoint()
        # print(info)
        processed_info, source = method(info)
        # print(processed_info,source)
        # breakpoint()
        self.identifier.processorFix(source)
        return processed_info

    def produce_some_content(self, processed_info):
        # print(processed_info)
        # print(self.methodsList['producer'])
        # breakpoint()
        content, source = self.methodsList["producer"](processed_info)
        self.identifier.producerFix(source)
        return content

    def post_some_content(self, content):
        posted_location, source = self.methodsList["poster"](content)
        self.identifier.posterFix(source)
        return posted_location

    def collect_some_feedback(self, posted_location):
        feedback, source = self.methodsList["feedback"](posted_location)
        self.identifier.feedbackFix(source)
        return feedback

    def optimize_topic_by_feedback(self, topic, feedback):
        optimized_result, source = self.methodsList["optimizer"](topic, feedback)
        self.identifier.optimizerFix(source)
        return feedback

    def update_optimized_result(self, optimized_result):
        update_result, source = self.methodsList["updator"](optimized_result)
        if type(update_result) == GeneratorType:
            for _ in update_result:
                ...  # to fix not iterating bug.
        self.identifier.updatorFix(source)

    def main(self):
        topic = self.get_one_topic()
        info = self.get_some_info(topic)
        processed_info = self.process_some_info(info)
        # print("PROCESSED_INFO: %s" % processed_info)
        # breakpoint()
        content = self.produce_some_content(processed_info)
        posted_location = self.post_some_content(content)
        feedback = self.collect_some_feedback(posted_location)
        optimized_result = self.optimize_topic_by_feedback(topic, feedback)
        self.update_optimized_result(optimized_result)


class ContentReviewer(ContentProducer):
    def __init__(self):
        super().__init__()
        self.identifier.typeFix(type(self).__name__)
        self.methodsList.update(
            {
                "fetcher": dummyFetcher,
                "reviewer": dummyReviewer,
                "reviewOptimizer": dummyReviewOptimizer,
            }
        )

    def fetch_some_content(self, topic):
        (posted_location, content), source = self.methodsList["fetcher"](topic)
        self.identifier.fetcherFix(source)
        return posted_location, content

    def review_content(self, content):
        review, source = self.methodsList["reviewer"](content)
        self.identifier.reviewerFix(source)
        return review

    def optimize_topic_by_feedback_review(self, topic, feedback, review):
        optimized_result, source = dummyReviewOptimizer(topic, feedback, review)
        return optimized_result  # this with instant feedback.

    def main(self, skip_review=False):
        if self.trash_location is not None:
            print("dumping trash at:\n{}".format(self.trash_location))
            dumpTrashDir(self.trash_location)
        topic = self.get_one_topic()
        # print("fetched topic:", topic)
        protocol, content = self.fetch_some_content(topic)  # dummy since here.
        # print("fetched protocol:", protocol)
        # print("fetched content:", content)
        if not skip_review:
            review = self.review_content(content)  # dummy reviewer.
            # print("reviewed content:", review)
        else:
            review = {key: [] for key in content.keys()}  # test feedback
            # of course nothing will be there.

        feedback = self.collect_some_feedback(review)  # instant feedback.
        # print("fetched feedback:", feedback)
        # breakpoint()
        if self.log_location is not None:
            mtype0, mcontent = jsonPrettyPrint(review)
            mtype1, mfeedback_content = jsonPrettyPrint(feedback)
            mtype0 = "log" if mtype0 != "json" else mtype0
            mtype1 = "log" if mtype0 != "json" else mtype1

            timestamp = getTimestamp()
            timestamp = str(timestamp).replace(".", "_")
            logName = "{}.{}".format(timestamp, mtype0)
            feedback_logName = "{}_feedback.{}".format(timestamp, mtype1)
            writeFileWithPath(
                self.log_location, logName, mcontent, "w+", encoding="utf-8"
            )
            writeFileWithPath(
                self.log_location,
                feedback_logName,
                mfeedback_content,
                "w+",
                encoding="utf-8",
            )

        # feedback is non-existant for local files.
        optimized_result = self.optimize_topic_by_feedback_review(
            topic, feedback, review
        )
        self.update_optimized_result(optimized_result)
