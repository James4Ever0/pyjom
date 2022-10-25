# serve my video, serve my cat video, dog video, set priority, serve others video
# by means of query? or just directly ask me for it.

# you'd better mimic the video that you have never recommend, and these audience have never seen before.
import sys

sys.path.append("/root/Desktop/works/pyjom/")
# you might want to add this to bilibili platform api, if there's no use of pyjom.commons
from pyjom.platforms.bilibili.credentials import getCredentialByDedeUserId

# from pyjom.platforms.bilibili.searchDataParser import parseSearchVideoResult # but you never use this shit.

# will it load the overheads of pyjom.commons?

# updated anyio. does that work? will it break dependencies?

import pyjq

from bilibili_api import sync, search, user, video

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
def getUserObject(dedeuserid: str = "397424026", use_credential: bool = False):
    dedeuserid_int = int(dedeuserid)
    if use_credential:
        credential = getCredentialByDedeUserId(
            dedeuserid
        )  # this will cache the cookies. so it allows multiple accounts.
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


@refresh_status_decorator  # this might prevent you adding the decorator everywhere?
@lru_cache(maxsize=1)
def getBilibiliVideoDatabase():
    db_dir = Path(getHomeDirectory()) / ".bilibili_video"
    if not os.path.exists(db_dir):
        os.mkdir(db_dir)
    db_path = db_dir / "database.db"  # sure this works?
    db = SqliteDatabase(db_path)
    return db


class BilibiliUser(Model):
    username = CharField()
    user_id = IntegerField(unique=True)
    is_mine = BooleanField(default=False)


class BilibiliVideo(Model):
    bvid = CharField(unique=True)
    visible = BooleanField()
    last_check = DateTimeField()  # well this is not tested. test it!
    poster = ForeignKeyField(
        BilibiliUser, field=BilibiliUser.user_id
    )  # is it my account anyway?
    description=CharField()
    play=CharField()
    pic=CharField()
    length = IntegerField()
    review = IntegerField() # you want to update? according to this?


def bilibiliTimecodeToSeconds(bilibili_timecode: str):
    import vtc

    timecode = "{}:0".format(bilibili_timecode)
    decimal_seconds = vtc.Timecode(timecode, rate=1).seconds
    seconds = round(decimal_seconds)
    return seconds


# @refresh_status_decorator
def searchVideos(
    query: str,
):  # what do you expect? you want the xml object let's get it!
    # search the thing directly? or you distill keywords from it?
    # or you use some baidu magic?
    # anyway, let's begin.
    # warning: this is coroutine.
    # you might want some magic. with 'suppressException' and pickledFunction?
    search_type = search.SearchObjectType.VIDEO
    params = {"duration": BSP.all.duration._10分钟以下}
    result = sync(search.search_by_type(query, search_type, params=params))
    # numPages = result["numPages"]  # usually we select the topmost candidates.
    # print(result)
    # you can use the upic to render some deceptive ads, but better not?
    mresult = pyjq.all(
        ".result[] | {mid, author, pic, play, is_pay, duration, bvid, description, title, pubdate, tag,typename, typeid, review, favorites, danmaku, rank_score, like, upic} | select (.title != null and .bvid != null)",
        result,
    )
    # so you want to persist these results or not?
    # better persist so we can reuse.
    # no persistance?
    # check some interesting result.
    return mresult
    # no selection?
    # you should use the parser found elsewhere. or not?
    # breakpoint()
    # remove keyword highlight from title. will you?
    # result['result'][0].keys()
    # keys = [
    #     "type",
    #     "id",
    #     "author",
    #     "mid",
    #     "typeid",
    #     "typename",
    #     "arcurl",
    #     "aid",
    #     "bvid",
    #     "title",
    #     "description",
    #     "arcrank",
    #     "pic",
    #     "play",
    #     "video_review",
    #     "favorites",
    #     "tag",
    #     "review",
    #     "pubdate",
    #     "senddate",
    #     "duration",
    #     "badgepay",
    #     "hit_columns",
    #     "view_type",
    #     "is_pay",
    #     "is_union_video",
    #     "rec_tags",
    #     "new_rec_tags",
    #     "rank_score",
    #     "like",
    #     "upic",
    #     "corner",
    #     "cover",
    #     "desc",
    #     "url",
    #     "rec_reason",
    #     "danmaku",
    # ]
    # rank score is important!


# you need my credential!
# better reuse the code.


def checkVideoInDatabase(bvid: str):
    # we use peewee (of course our modified version)
    db = getBilibiliVideoDatabase()
    db.create_tables([BilibiliVideo, BilibiliUser])
    result = BilibiliVideo.get_or_none(BilibiliVideo.bvid == bvid)
    return result  # check it elsewhere?


# get my videos first!
import math

# @refresh_status_decorator
from bilibili_api.user import VideoOrder


def getMyVideos(
    tid=0, keyword="", order=VideoOrder.PUBDATE
):  # all videos? just at init.
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
    stopped = False
    while not stopped:
        videos = sync(user.get_videos(pn=pn))
        print(videos)
        # dict_keys(['list', 'page', 'episodic_button', 'is_risk', 'gaia_res_type', 'gaia_data'])
        page = videos["page"]  # pagination options
        numPages = math.ceil(page["count"] / page["ps"])
        topicList = videos["list"]["tlist"]
        # {'1': {'tid': 1, 'count': 13, 'name': '动画'}, '160': {'tid': 160, 'count': 257, 'name': '生活'}, '181': {'tid': 181, 'count': 2, 'name': '影视'}, '188': {'tid': 188, 'count': 4, 'name': '科技'}, '217': {'tid': 217, 'count': 4, 'name': '动物圈'}, '234': {'tid': 234, 'count': 1, 'name': '运动'}, '3': {'tid': 3, 'count': 9, 'name': '音乐'}, '36': {'tid': 36, 'count': 30, 'name': '知识'}, '4': {'tid': 4, 'count': 67, 'name': '游戏'}}

        # breakpoint()
        video_list = videos["list"]["vlist"]
        for video in video_list:
            bvid = video["bvid"]
            result = checkVideoInDatabase(bvid)
            if result:
                stopped = True
                break
        # videos['list']['vlist'][0].keys()
        # dict_keys(['comment', 'typeid', 'play', 'pic', 'subtitle', 'description', 'copyright', 'title', 'review', 'author', 'mid', 'created', 'length', 'video_review', 'aid', 'bvid', 'hide_click', 'is_pay', 'is_union_video', 'is_steins_gate', 'is_live_playback'])
        pn += 1


def searchMyVideos():
    # better use semantic search. but now we use hybrid search instead.
    # hybrid search: metatopic plus bm25
    # how to search my video? and how to measure relevance?
    ...


# you can make excerpt from video to lure people into viewing your video.

# no need to decorate this thing. only put some 'unchecked' video into array.
def registerMyVideo(
    bvid: str, user_id: int
):  # this is the video i just post. must be regularly checked then add to candidate list. you can check it when another call for my videos has been issued.
    # register user first, then register the video.
    ...


def checkRegisteredVideo():
    # check if they are published or not.
    ...

# seems bilibili can automatically categorize video.
# we just need to find out how?
def checkPublishedVideo(bvid:str):
    # check if video is still visible or taken down.
    # if video is not visible then we delete this video from database.
    v= video.Video(bvid=bvid)
    info = sync(v.get_info()) # getting shit? we need some normal video for test.
    print(info)
    # dict_keys(['bvid', 'aid', 'videos', 'tid', 'tname', 'copyright', 'pic', 'title', 'pubdate', 'ctime', 'desc', 'desc_v2', 'state', 'duration', 'forward', 'rights', 'owner', 'stat', 'dynamic', 'dimension', 'premiere', 'teenage_mode', 'is_chargeable_season', 'is_story', 'no_cache', 'subtitle', 'is_season_display', 'user_garb', 'honor_reply', 'like_icon'])
    #  'state': -4,
    breakpoint()
    # we use some random video for test.


# i suggest you to use sqlalchemy. since this is no ordinary task.
# you cannot just check every video of your own in the past.

## following code is for test purpose.

if __name__ == "__main__":
    # query = "cod19"  # recent hot videos.
    # results = searchVideos(query)
    # no keywords? are you kidding?
    # results = getMyVideos()
    # print(results)
    video_bvid_invisible = "BV1x84y1B7Nb"
    video_bvid_visible = "BV1Fs411k7e9" # 老戴的视频
    # 啊叻？视频不见了？
    # checkPublishedVideo(video_bvid_invisible)
    checkPublishedVideo(video_bvid_visible)
    # 视频撞车了 需要原创视频哦