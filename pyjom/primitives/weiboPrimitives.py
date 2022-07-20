from pyjom.main import *
from pyjom.commons import *
# this is a reviewer, not a poster.
# you may create interface to label the content and automate the stuff altogether.


class WeiboPetsReviewer(ContentReviewer):
    def __init__(self, enable_log=True, auto=False,semiauto=True, dummy_auto=True,
        template_names=[],args={},basedir="/dev/shm/sina",autopurge=True):
        super().__init__()
        if enable_log:
            self.log_location = "logs/sina/pets/"
        if autopurge:
            shutil.rmtree(basedir)
        self.identifier.typeFix(type(self).__name__)
        self.methodsList.update(
            {
                "topic": petsTopicGenerator,
                "fetcher": weiboFetcher,
                "reviewer": keywordDecorator(weiboSearchReviewer, basedir=basedir,auto=auto,semiauto=semiauto,dummy_auto=dummy_auto,template_names=template_names,args=args),
                "feedback": weiboFeedback,
            }
        )
