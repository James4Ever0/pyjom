import types
from bilibili_api import sync

# wtf is async generator type?
def bilibiliSync(func):
    def wrapper(*args, **kwargs):
        coroutineMaybe=func(*args, **kwargs)
        if type(coroutineMaybe) == types.CoroutineType:
            return sync(unknownObject)
        else:
            return func(*args, **kwargs)
    return wrapper
