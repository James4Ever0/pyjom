import types
from bilibili_api import sync

# wtf is async generator type?
def bilibiliSync(func):
    def wrapper(*args, **kwargs):
        if type(func) == types.:
            return sync(func(*args, **kwargs))
        else:
            return func(*args, **kwargs)
    return wrapper
