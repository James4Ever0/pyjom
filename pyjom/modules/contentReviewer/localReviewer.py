from pyjom.commons import *
from pyjom.modules.contentCensoring.core import localCensor
import json


def filesystemReviewerNoGenerator

@decorator
def filesystemReviewer(
    content, auto=False, semiauto=True, dummy_auto=True, args={}, template_names=[], generator:bool=False
):
    # print(content)
    # print('generator flag', generator)
    # link = content["link"]
    # if not generator:
    mreview = []
    for elem in content:
        mreview.append(reviewResult)
    return mreview
