# serve my video, serve my cat video, dog video, set priority, serve others video
# by means of query? or just directly ask me for it.

# you'd better mimic the video that you have never recommend, and these audience have never seen before.
import sys
sys.path.append("/root/Desktop/works/pyjom/")
# you might want to add this to bilibili platform api, if there's no use of pyjom.commons
from pyjom.platforms.bilibili.credentials import getCredentialByDedeUserId
from pyjom.platforms.bilibili.searchDataParser import parseSearchVideoResult
# will it load the overheads of pyjom.commons?

# updated anyio. does that work? will it break dependencies?

import pyjq

from bilibili_api import sync, search, user

from peewee import *

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
        credential = getCredentialByDedeUserId(dedeuserid) # this will cache the cookies. so it allows multiple accounts.
    else:
        credential = None
    u = user.User(dedeuserid_int, credential=credential)
    return u

from lazero.filesystem.env import getHomeDirectory
from pathlib import Path
import os

from peewee import *

def refresh_status():
    return

refresh_status()
schedule.every(20).minutes.do(refresh_status)

def refresh_status_decorator(func):
    def wrapper(*args, **kwargs):
        schedule.run_pending()
        return func(*args, **kwargs)
    return wrapper

@refresh_status_decorator # this might prevent you adding the decorator everywhere?
@lru_cache(maxsize=1)
def getBilibiliVideoDatabase():
    db_dir = Path(getHomeDirectory()) / ".bilibili_video"
    if not os.path.exists(db_dir):
        os.mkdir(db_dir)
    db_path = db_dir /"database.db" # sure this works?
    db = SqliteDatabase(db_path)
    return db

class BilibiliUser(Model):
    username = CharField()
    user_id = IntegerField(unique=True)
    is_mine = BooleanField(default=False)

class BilibiliVideo(Model):
    bvid = CharField(unique=True)
    visible = BooleanField()
    last_check = DateTimeField() # well this is not tested. test it!
    poster = ForeignKeyField(BilibiliUser, field=BilibiliUser.user_id) # is it my account anyway?


# @refresh_status_decorator
def searchVideos(query:str): # what do you expect? you want the xml object let's get it!
    # search the thing directly? or you distill keywords from it?
    # or you use some baidu magic?
    # anyway, let's begin.
    # warning: this is coroutine.
    # you might want some magic. with 'suppressException' and pickledFunction?
    search_type = search.SearchObjectType.VIDEO
    params = {"duration": BSP.all.duration._10分钟以下}
    result = sync(search.search_by_type(query,search_type, params=params))
    numPages = result['numPages'] # usually we select the topmost candidates.
    print(result)
    # you should use the parser found elsewhere. or not?
    breakpoint()
    # remove keyword highlight from title. will you?
    # result['result'][0].keys()
    # dict_keys(['type', 'id', 'author', 'mid', 'typeid', 'typename', 'arcurl', 'aid', 'bvid', 'title', 'description', 'arcrank', 'pic', 'play', 'video_review', 'favorites', 'tag', 'review', 'pubdate', 'senddate', 'duration', 'badgepay', 'hit_columns', 'view_type', 'is_pay', 'is_union_video', 'rec_tags', 'new_rec_tags', 'rank_score', 'like', 'upic', 'corner', 'cover', 'desc', 'url', 'rec_reason', 'danmaku'])

# you need my credential!
# better reuse the code.


def checkVideoInDatabase(bvid:str):
    # we use peewee (of course our modified version)
    db = getBilibiliVideoDatabase()
    db.create_tables([BilibiliVideo, BilibiliUser])
    result = BilibiliVideo.get_or_none(BilibiliVideo.bvid == bvid)
    return result # check it elsewhere?

# get my videos first!
# @refresh_status_decorator
def getMyVideos(): # all videos? just at init.
    # some stop condition for early termination.
    # if any of the video exists in the database, we stop this shit.
    user = getUserObject()
    pn = 1
    # tid	int, optional	分区 ID. Defaults to 0（全部）
    # pn	int, optional	页码，从 1 开始. Defaults to 1.
    # ps	(int, optional)	每一页的视频数. Defaults to 30.
    # keyword	str, optional	搜索关键词. Defaults to "".
    # order	VideoOrder, optional	排序方式. Defaults to VideoOrder.PUBDATE
    # this is async. use sync.
    while True:
        videos = sync(user.get_videos(pn=pn))
        print(videos)
        breakpoint()
        pn +=1


def searchMyVideos():
    # better use semantic search. but now we use hybrid search instead.
    # hybrid search: metatopic plus bm25
    # how to search my video? and how to measure relevance?
    ...

# no need to decorate this thing. only put some 'unchecked' video into array.
def registerMyVideo(bvid:str,user_id:int): # this is the video i just post. must be regularly checked then add to candidate list. you can check it when another call for my videos has been issued.
    # register user first, then register the video.
    ...

def checkRegisteredVideo():
    # check if they are published or not.
    ...

def checkPublishedVideo():
    # check if video is still visible or taken down.
    # if video is not visible then we delete this video from database.
    ...

# i suggest you to use sqlalchemy. since this is no ordinary task.
# you cannot just check every video of your own in the past.

## following code is for test purpose.

if __name__ == '__main__':
    query = "cod19" # recent hot videos.
    results = searchVideos(query)