import types
from bilibili_api import sync

# wtf is async generator type?
def bilibiliSync(func):
    def wrapper(*args, **kwargs):
        coroutineMaybe=func(*args, **kwargs)
        if type(coroutineMaybe) == types.CoroutineType:
            return sync(coroutineMaybe)
        else:
            return coroutineMaybe
    return wrapper
