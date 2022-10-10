import types
from bilibili_api import sync
def bilibiliSync(func):
    def wrapper(*args, **kwargs):
        if type(func) == types.CoroutineType