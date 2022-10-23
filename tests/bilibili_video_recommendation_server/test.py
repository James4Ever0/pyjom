# serve my video, serve my cat video, dog video, set priority, serve others video
# by means of query? or just directly ask me for it.

# you'd better mimic the video that you have never recommend, and these audience have never seen before.
import sys
sys.path.append("/root/Desktop/works/pyjom/")
# you might want to add this to bilibili platform api, if there's no use of pyjom.commons
from pyjom.platforms.bilibili.credentials import getCredentialByDedeUserId


from bilibili_api import sync, search, user


BSP = search.bilibiliSearchParams
# you can query for the server status.
# make it into a dashboard like thing.

# also make a decorator for refreshing status, add it to every function.
# thie refresher is scheduled.
# you may want to run this beforehand...

import schedule

# do we really need credential for checking our video? you can try.
from functools import lru_cache

@lru_cache(maxsize=1)
def getUserObject(dedeuserid:str="397424026", use_credential:bool=False):
    dedeuserid_int = int(dedeuserid)
    if use_credential:
        credential = getCredentialByDedeUserId(dedeuserid)
    else:
        credential = None
    u = user.User(dedeuserid_int, credential=credential)
    return u


def refresh_status():
    ...

refresh_status()
schedule.every(20).minutes.do(refresh_status)

def refresh_status_decorator(func):
    def wrapper(*args, **kwargs):
        schedule.run_pending()
        return func(*args, **kwargs)
    return wrapper

@refresh_status_decorator
def searchVideos(query:str): # what do you expect? you want the xml object let's get it!
    # search the thing directly? or you distill keywords from it?
    # or you use some baidu magic?
    # anyway, let's begin.
    # warning: this is coroutine.
    # you might want some magic. with 'suppressException' and pickledFunction?
    search_type = search.SearchObjectType.VIDEO
    params = {"duration": BSP.all.duration._10分钟以下}
    result = sync(search.search_by_type(query,search_type, params=params))

# you need my credential!
# better reuse the code.

videos first!

def getMyVideos():
@refresh_status_decorator
def searchMyVideos():
    # better use semantic search. but now we use hybrid search instead.
    # hybrid search: metatopic plus bm25



# no need to decorate this thing. only put some 'unchecked' video into array.
def submitMyVideo(): # this is the video i just post. must be regularly checked then add to candidate list. you can check it when another call for my videos has been issued.