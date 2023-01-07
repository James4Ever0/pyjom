from pyjom.commons import *


@decorator
def dummyProducer(processed_info):
    return {
        "husky": {
            "title": "<a million husky videos>",
            "article": "husky is so darn cute",
            "video": "<myvideo>",
            "summary": "this is my husky",
        }
    }
