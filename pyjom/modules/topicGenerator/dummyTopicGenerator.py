from reloading import reloading
from pyjom.commons import *


@decorator
@reloading
def dummyTopic():
    return "pets"


@decorator
@reloading
def metaTopic(selected_source):
    sources = {
        "baidu_baijiahao": ["shitty title1"],
        "bilibili_trending": ["boy with women's clothes"],
    }
    return sources[selected_source]
