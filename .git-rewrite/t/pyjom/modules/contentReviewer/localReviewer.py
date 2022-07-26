from pyjom.commons import *
from pyjom.modules.contentCensoring.core import localCensor
import json


@decorator
def filesystemReviewer(
    content, auto=False, semiauto=True, dummy_auto=True, args={}, template_names=[]
):
    # print(content)
    # link = content["link"]
    mreview = []
    for elem in content:
        print("element inside:")
        print("_" * 20)
        _, pretty_printed = jsonPrettyPrint(elem)
        print(pretty_printed)
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
        mreview.append({"review": review, "source": source})
    return mreview
