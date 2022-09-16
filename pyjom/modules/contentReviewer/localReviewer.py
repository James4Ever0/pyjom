from pyjom.commons import *
from pyjom.modules.contentCensoring.core import localCensor
import json

def filesystemReviewerCoreAnalyzer(elem,auto=False, semiauto=True, dummy_auto=True, args={}, template_names=[]):
    print("element inside:")
    print("_" * 20)
    _, pretty_printed = jsonPrettyPrint(elem)
    print(pretty_printed)
    print("ELEMENT", elem)
    breakpoint()
    review, source = localCensor(
        elem,
        auto=auto,
        semiauto=semiauto,
        dummy_auto=dummy_auto,
        args=args,
        template_names=template_names,
    )  # unnoticed source.
    print("review:")
    # breakpoint()
    print(json.dumps(review, indent=4))
    reviewResult = {"review": review, "source": source}
    return reviewResult

def filesystemReviewerNoGenerator(content,auto=False, semiauto=True, dummy_auto=True, args={}, template_names=[] ):
    mreview = []
    for elem in content:
        reviewResult = filesystemReviewerCoreAnalyzer(content,    auto=auto,
        semiauto=semiauto,
        dummy_auto=dummy_auto,
        args=args,
        template_names=template_names)
        mreview.append(reviewResult)
    return mreview

@decorator
def filesystemReviewer(
    content, auto=False, semiauto=True, dummy_auto=True, args={}, template_names=[], generator:bool=False
):
    # print(content)
    # print('generator flag', generator)
    # link = content["link"]
    # if not generator:

