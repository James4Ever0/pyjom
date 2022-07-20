from pyjom.commons import *
from pyjom.modules.contentCensoring.core import weiboCensor
import json


@decorator
def weiboSearchReviewer(content, basedir=None, auto=False, semiauto=True,dummy_auto=True,template_names=[], args={}):
    mreview = {}
    for key in content.keys():
        print("keyword:", key)
        print("_" * 20)
        mreview[key] = []
        mcontent = content[key]
        for elem in mcontent:
            print("element inside:")
            print("_" * 20)
            meta = elem["meta"]
            feedback = elem["feedback"]
            _, pretty_printed = jsonPrettyPrint(elem)
            print(pretty_printed)
            review, source = weiboCensor(
                elem, basedir=basedir, semiauto=semiauto, auto=auto, dummy_auto=dummy_auto,template_names=template_names ,args=args
            )  # unnoticed source.
            review["meta"] = meta
            review["feedback"] = feedback
            print("review:", review)
            mreview[key].append({"review": review, "source": source})
    return mreview
