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


@lru_cache(maxsize=3)  # could be bigger.
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


class BilibiliUser(Model):
    username = CharField()
    user_id = IntegerField(unique=True)
    is_mine = BooleanField(default=False)
    followers = IntegerField(
        null=True
    )  # how to get that? every time you get some video you do this shit? will get you blocked.
    # well you can check it later.
    avatar = CharField(null=True)  # warning! charfield max length is 255


class BilibiliVideo(Model):
    bvid = CharField(unique=True)
    visible = BooleanField(null=True) # are you sure?
    last_check = DateTimeField()  # well this is not tested. test it!
    poster = ForeignKeyField(
        BilibiliUser, field=BilibiliUser.user_id
    )  # is it my account anyway?
    description = CharField(max_length=350)  # will it work?
    play = IntegerField(null=True)
    pic = CharField()
    length = IntegerField()
    review = IntegerField(null=True)  # you want to update? according to this?


def refresh_status_decorator(func):
    def wrapper(*args, **kwargs):
        schedule.run_pending()
        return func(*args, **kwargs)
    return wrapper


@lru_cache(maxsize=1)
def getBilibiliVideoDatabase():
    db_dir = Path(getHomeDirectory()) / ".bilibili_video"
    if not os.path.exists(db_dir):
        os.mkdir(db_dir)
    db_path = db_dir / "database.db"  # sure this works?
    db = SqliteDatabase(db_path)
    return db

def getBilibiliVideoDatabaseAndCreateTables():
    db = getBilibiliVideoDatabase()
    db.create_tables([BilibiliUser, BilibiliVideo])
    return db

def refresh_status():
    # what to do? just select and update?
    # but you need the database object. it is loop dependency!
    # well we can split the function.
    db = getBilibiliVideoDatabaseAndCreateTables()
    return


refresh_status()
schedule.every(20).minutes.do(refresh_status)


@refresh_status_decorator  # this might prevent you adding the decorator everywhere?
def getBilibiliVideoDatabaseCreateTablesAndRefreshStatus():
    db = getBilibiliVideoDatabaseAndCreateTables()
    return db


def bilibiliTimecodeToSeconds(bilibili_timecode: str):
    import vtc
    timecode = "{}:0".format(bilibili_timecode)
    decimal_seconds = vtc.Timecode(timecode, rate=1).seconds
    seconds = round(decimal_seconds)
    return seconds


# @refresh_status_decorator
def searchVideos(
    query: str,
    iterate: bool = False,
    page_start: int = 1,
    params={"duration": BSP.all.duration._10分钟以下},  # is that right? maybe?
    search_type=search.SearchObjectType.VIDEO,
):  # what do you expect? you want the xml object let's get it!
    # search the thing directly? or you distill keywords from it?
    # or you use some baidu magic?
    # anyway, let's begin.
    # warning: this is coroutine.
    # you might want some magic. with 'suppressException' and pickledFunction?
    def getResultParsed(result):
        mresult = pyjq.all(
            ".result[] | {mid, author, pic, play, is_pay, duration, bvid, description, title, pubdate, tag, typename, typeid, review, favorites, danmaku, rank_score, like, upic} | select (.title != null and .bvid != null)",
            result,
        )
        return mresult

    def getResult(page):
        result = sync(
            search.search_by_type(query, search_type, params=params, page=page)
        )
        return result

    result = getResult(page_start)
    numPages = result["numPages"]  # usually we select the topmost candidates.
    # print(result)
    if numPages < page_start:
        page_start_current = 1
    else:
        page_start_current = page_start
        mresult = getResultParsed(result)
        for v in mresult:
            yield v
    if not iterate:
        page_range = range(page_start_current, page_start_current + 1)
    else:
        page_range = range(page_start_current, numPages + 1)
    for page in page_range:
        if page != page_start:
            result = getResult(page)
            mresult = getResultParsed(result)
            for v in mresult:
                yield v
    # you can use the upic to render some deceptive ads, but better not?

    # so you want to persist these results or not?
    # better persist so we can reuse.
    # no persistance?
    # check some interesting result.

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


def getUserVideos(
    tid=0,
    keyword="",
    order=VideoOrder.PUBDATE,
    dedeuserid: str = "397424026",
    use_credential: bool = False,
    stop_on_duplicate: bool = True,
):  # all videos? just at init.
    # some stop condition for early termination.
    # if any of the video exists in the database, we stop this shit.
    u = getUserObject(dedeuserid=dedeuserid, use_credential=use_credential)
    pn = 1
    # tid	int, optional	分区 ID. Defaults to 0（全部）
    # pn	int, optional	页码，从 1 开始. Defaults to 1.
    # ps	(int, optional)	每一页的视频数. Defaults to 30.
    # keyword	str, optional	搜索关键词. Defaults to "".
    # order	VideoOrder, optional	排序方式. Defaults to VideoOrder.PUBDATE
    # this is async. use sync.
    stopped = False
    while not stopped:
        videos = sync(u.get_videos(pn=pn, keyword=keyword))
        print(videos)
        # dict_keys(['list', 'page', 'episodic_button', 'is_risk', 'gaia_res_type', 'gaia_data'])
        page = videos["page"]  # pagination options
        numPages = math.ceil(page["count"] / page["ps"])
        topicList = videos["list"]["tlist"]
        # {'1': {'tid': 1, 'count': 13, 'name': '动画'}, '160': {'tid': 160, 'count': 257, 'name': '生活'}, '181': {'tid': 181, 'count': 2, 'name': '影视'}, '188': {'tid': 188, 'count': 4, 'name': '科技'}, '217': {'tid': 217, 'count': 4, 'name': '动物圈'}, '234': {'tid': 234, 'count': 1, 'name': '运动'}, '3': {'tid': 3, 'count': 9, 'name': '音乐'}, '36': {'tid': 36, 'count': 30, 'name': '知识'}, '4': {'tid': 4, 'count': 67, 'name': '游戏'}}

        # breakpoint()
        video_list = videos["list"]["vlist"]
        for v in video_list:
            bvid = v["bvid"]
            result = checkVideoInDatabase(bvid)
            if result and stop_on_duplicate:
                stopped = True
                break
            yield v
        # videos['list']['vlist'][0].keys()
        # dict_keys(['comment', 'typeid', 'play', 'pic', 'subtitle', 'description', 'copyright', 'title', 'review', 'author', 'mid', 'created', 'length', 'video_review', 'aid', 'bvid', 'hide_click', 'is_pay', 'is_union_video', 'is_steins_gate', 'is_live_playback'])
        if page == numPages:
            break
        pn += 1


from typing import Union


def searchUserVideos(
    keyword: str,
    tid: int = 0,
    dedeuserid: str = "397424026",
    method: Union["online", "bm25", "contain"] = "online",
    use_credential: bool = False,
    videoOrder=VideoOrder.PUBDATE,
):  # you can support this in database?
    # you want keyword search or not? it's better than searching in database. i think.
    # but database search saves bandwidth.
    # better use semantic search. but now we use hybrid search instead.
    # hybrid search: metatopic plus bm25
    # or not?
    # just dump that shit.
    # check if keyword overlaps.
    # how to search my video? and how to measure relevance?
    if method == "online":
        for video in getUserVideos(
            tid=tid,
            keyword=keyword,
            dedeuserid=dedeuserid,
            use_credential=use_credential,
            stop_on_duplicate=False,
        ):
            ...
        # info = u.get_videos(keyword=keyword,order=videoOrder)
    elif method == "bm25":
        # export all video? shit?
        ...
    elif method == "contain":
        # use some builtin peewee method instead?
        ...


# you can make excerpt from video to lure people into viewing your video.

# no need to decorate this thing. only put some 'unchecked' video into array.
def registerMyVideo(
    bvid: str, user_id: int
):  # this is the video i just post. must be regularly checked then add to candidate list. you can check it when another call for my videos has been issued.
    # register user first, then register the video.
    # you will store it to database.
    info = getVideoInfo(bvid)



import datetime

# grace period to be one day. that's long enough. or not?
# we still need some more experiment.

# check api doc for hint.
def checkRegisteredVideo(
    bvid: str,
    grace_period=datetime.timedelta(days=1),
    check_interval=datetime.timedelta(hours=1),
):  # maybe the video is not immediately visible after registration.
    # check if they are published or not.
    ...
    # you can schedule check every hour. not all the time.
    # basically the same thing. but we do not delete these video till the time is too late, after check.


# seems bilibili can automatically categorize video.
# we just need to find out how?
def checkPublishedVideo(bvid: str):
    # if published, the video is taken down afterwards, we will delete it.
    # check if video is still visible or taken down.
    # if video is not visible then we delete this video from database.
    v = video.Video(bvid=bvid)
    info = sync(v.get_info())  # getting shit? we need some normal video for test.
    print(info)
    # dict_keys(['bvid', 'aid', 'videos', 'tid', 'tname', 'copyright', 'pic', 'title', 'pubdate', 'ctime', 'desc', 'desc_v2', 'state', 'duration', 'forward', 'rights', 'owner', 'stat', 'dynamic', 'dimension', 'premiere', 'teenage_mode', 'is_chargeable_season', 'is_story', 'no_cache', 'subtitle', 'is_season_display', 'user_garb', 'honor_reply', 'like_icon'])
    #  'state': -4,
    # bad state! what is the meaning of this state?
    # normal; state -> 0
    state = info["state"]
    visible = state == 0
    # info['stat'].keys()
    # dict_keys(['aid', 'view', 'danmaku', 'reply', 'favorite', 'coin', 'share', 'now_rank', 'his_rank', 'like', 'dislike', 'evaluation', 'argue_msg'])
    # breakpoint()
    # if anything goes wrong, do not return the state.
    # if you want update, better do it here. we are checking and updating the video.
    # we use some random video for test.


# i suggest you to use sqlalchemy. since this is no ordinary task.
# you cannot just check every video of your own in the past.

## following code is for test purpose.

# shall write some server.
# not fastapi!


if __name__ == "__main__":
    query = "cod19"  # recent hot videos.
    results = searchVideos(query)
    for v in results:
        print(v)
    # no keywords? are you kidding?
    # results = getMyVideos()
    # print(results)
    # video_bvid_invisible = "BV1pd4y1y7cu"  # too fucking fast. i can't see shit.
    # # some hard rule on this? like being invisible for how long we will disable video source for good?
    # video_bvid_abnormal = "BV1x84y1B7Nb"
    # video_bvid_visible = "BV1Fs411k7e9"  # 老戴的视频
    # # 啊叻？视频不见了？
    # checkPublishedVideo(video_bvid_invisible)
    # checkPublishedVideo(video_bvid_visible)
    # checkPublishedVideo(video_bvid_abnormal)
    # 视频撞车了 需要原创视频哦