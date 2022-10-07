from pyjom.commons import *


@decorator
def petsTopicGenerator():
    # this is just some primitive topic, always return the same thing.
    # topics cannot be multilingual.
    return {"entities": [{"chinese": "搞笑 宠物", "english": "funny pets"}]}
