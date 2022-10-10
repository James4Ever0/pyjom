import types
from bilibili_api import sync

# wtf is async generator type?
def bilibiliSync(func):
    def wrapper(*args, **kwargs):
        if type(func) == types.CoroutineType:
            return sync(func(*args, **kwargs)
