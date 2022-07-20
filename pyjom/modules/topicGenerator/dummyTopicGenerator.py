from pyjom.commons import *


@decorator
def dummyTopic():
    return "pets"


@decorator
def metaTopic(selected_source):
    sources = {
        "baidu_baijiahao": ["shitty title1"],
        "bilibili_trending": ["boy with women's clothes"],
    }
    return sources[selected_source]
