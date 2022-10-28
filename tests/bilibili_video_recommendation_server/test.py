# serve my video, serve my cat video, dog video, set priority, serve others video
# by means of query? or just directly ask me for it.

# you'd better mimic the video that you have never recommend, and these audience have never seen before.
import time
import sys
import datetime

sys.path.append("/root/Desktop/works/pyjom/")
# you might want to add this to bilibili platform api, if there's no use of pyjom.commons
from pyjom.platforms.bilibili.credentials import getCredentialByDedeUserId
from pyjom.platforms.bilibili.utils import linkFixer, videoDurationStringToSeconds

# from pyjom.platforms.bilibili.searchDataParser import parseSearchVideoResult # but you never use this shit.

# will it load the overheads of pyjom.commons?

# updated anyio. does that work? will it break dependencies?

import pyjq

from bilibili_api import sync, search, user, video

from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase, FTSModel, SearchField, RowIDField

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
    visible = BooleanField(null=True)  # are you sure?
    last_check = DateTimeField(default=datetime.datetime.now)  # well this is not tested. test it!
    register_date = DateTimeField(default=datetime.datetime.now)
    poster = ForeignKeyField(
        BilibiliUser, field=BilibiliUser.user_id
    )  # is it my account anyway?
    play = IntegerField(null=True)
    pic = CharField(null=True)
    length = IntegerField(null=True)
    pubdate = IntegerField(default=0)
    review = IntegerField(null=True)  # you want to update? according to this?
    favorites = IntegerField(default=0)


class BilibiliVideoIndex(FTSModel):
    rowid = RowIDField()  # this does not support
    title = SearchField()
    tag= SearchField()
    description = SearchField()

    class Meta:
        database = None  # that's good.
        options = {"tokenize": "porter"}  # you need manually separate some


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
    # db = SqliteDatabase(db_path)
    db = SqliteExtDatabase(
        db_path, pragmas={"journal_mode": "wal", "cache_size": -1024 * 64}
    )
    # test the full text search function elsewhere. please?
    return db


def getBilibiliVideoDatabaseAndCreateTables():
    db = getBilibiliVideoDatabase()
    db.create_tables([BilibiliUser, BilibiliVideo, BilibiliVideoIndex])
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


# @refresh_status_decorator
def searchVideos(
    query: str,
    iterate: bool = False,
    page_start: int = 1,
    params={"duration": BSP.all.duration._10分钟以下},  # is that right? maybe?
):  # what do you expect? you want the xml object let's get it!
    # search the thing directly? or you distill keywords from it?
    search_type=search.SearchObjectType.VIDEO
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
    use_credential: bool =False,
    stop_on_duplicate: bool = True,
    sleep:int=2,
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
        # print(videos)
        # dict_keys(['list', 'page', 'episodic_button', 'is_risk', 'gaia_res_type', 'gaia_data'])
        page = videos["page"]  # pagination options
        numPages = math.ceil(page["count"] / page["ps"])
        # print('NUM PAGES',numPages)
        topicList = videos["list"]["tlist"]
        # {'1': {'tid': 1, 'count': 13, 'name': '动画'}, '160': {'tid': 160, 'count': 257, 'name': '生活'}, '181': {'tid': 181, 'count': 2, 'name': '影视'}, '188': {'tid': 188, 'count': 4, 'name': '科技'}, '217': {'tid': 217, 'count': 4, 'name': '动物圈'}, '234': {'tid': 234, 'count': 1, 'name': '运动'}, '3': {'tid': 3, 'count': 9, 'name': '音乐'}, '36': {'tid': 36, 'count': 30, 'name': '知识'}, '4': {'tid': 4, 'count': 67, 'name': '游戏'}}
        # breakpoint()
        video_list = videos["list"]["vlist"]
        # breakpoint()
        if video_list == []: break
        for v in video_list:
            bvid = v["bvid"]
            result = checkVideoInDatabase(bvid)
            if result and stop_on_duplicate:
                stopped = True
                break
            # print(v)
            # dict_keys(['comment', 'typeid', 'play', 'pic', 'subtitle', 'description', 'copyright', 'title', 'review', 'author', 'mid', 'created', 'length', 'video_review', 'aid', 'bvid', 'hide_click', 'is_pay', 'is_union_video', 'is_steins_gate', 'is_live_playback'])
            # breakpoint()
            yield v['bvid'], v[''], v['']
        # videos['list']['vlist'][0].keys()
        # dict_keys(['comment', 'typeid', 'play', 'pic', 'subtitle', 'description', 'copyright', 'title', 'review', 'author', 'mid', 'created', 'length', 'video_review', 'aid', 'bvid', 'hide_click', 'is_pay', 'is_union_video', 'is_steins_gate', 'is_live_playback'])
        if page >= numPages:
            break
        time.sleep(sleep)
        pn += 1


from typing import Literal


def searchUserVideos(
    keyword: str,
    tid: int = 0,
    dedeuserid: str = "397424026",
    method: Literal["online", "bm25"] = "online",
    use_credential: bool = False,
    videoOrder=VideoOrder.PUBDATE,  # FAVOURITE, VIEW
    limit: int = 10,
):  # you can support this in database?
    # you want keyword search or not? it's better than searching in database. i think.
    # but database search saves bandwidth.
    # better use semantic search. but now we use hybrid search instead.
    # hybrid search: metatopic plus bm25
    # or not?
    # just dump that shit.
    # check if keyword overlaps.
    # how to search my video? and how to measure relevance?
    resultList = []
    if method == "online":
        for video_index, bvid, cover in getUserVideos(
            tid=tid,
            keyword=keyword,
            dedeuserid=dedeuserid,
            use_credential=use_credential,
            stop_on_duplicate=False,
        ):
            # what is the content? plan to update?
            # print("SEARCHED USER VIDEO ID:", v_id)
            order = None
            resultList.append(((video_index, bvid, cover), order))
        # info = u.get_videos(keyword=keyword,order=videoOrder)
    elif method == "bm25":
        # export all video? shit?
        # you should tokenize the thing.
        # but this search does not have limitations!
        user_video_ids = [v.id for v in BilibiliVideo.select(dedeuserid=dedeuserid)]
        results = (
            BilibiliVideoIndex.search_bm25(keyword)
            .where(BilibiliVideoIndex.rowid in user_video_ids)
            .limit(limit)
        )
        for index, video_index in enumerate(results):
            bilibiliVideo = BilibiliVideo.get(id=video_index.id)
            # what is the count? you need to reorder?
            bvid = bilibiliVideo.bvid
            cover = bilibiliVideo.pic
            favorites = bilibiliVideo.favorites
            pubdate = bilibiliVideo.pubdate
            view = bilibiliVideo.play
            if videoOrder == VideoOrder.FAVORITE:
                order = -favorites
            elif videoOrder == VideoOrder.VIEW:
                order = -view
            elif videoOrder == VideoOrder.PUBDATE:
                order = -pubdate  # most recent video.
            else:
                order = index
            # you should return the video_index.
            resultList.append(((video_index, bvid, cover), order))
        resultList.sort(key=lambda x: x[1])
    for (video_index, bvid, cover), _ in resultList:
        yield video_index, bvid, cover  # this is bilibiliVideoIndex, but you also needs the bvid.


# you can make excerpt from video to lure people into viewing your video.

def getVideoInfo(bvid:str):
    v = video.Video(bvid=bvid)
    info = sync(v.get_info())
    return info

# no need to decorate this thing. only put some 'unchecked' video into array.
def registerMyVideo(
    bvid: str, dedeuserid:str
):  # this is the video i just post. must be regularly checked then add to candidate list. you can check it when another call for my videos has been issued.
    # register user first, then register the video.
    # you will store it to database.
    user_id = int(dedeuserid)
    u= BilibiliUser.get_or_none(user_id = user_id)
    if u is None:
        myUser = user.User(user_id)
        userInfo = sync(myUser.get_user_info())
        # print(userInfo)
        # print(dir(userInfo))
        # breakpoint()
        # dict_keys(['list', 're_version', 'total'])
        # in the 'list' we've got a few recent followers.
        followersInfo = sync(myUser.get_followers())
        username = userInfo['name']
        followers = followersInfo['total']
        avatar = userInfo['face']
        u, _ = BilibiliUser.get_or_create(user_id = user_id,username = username,is_mine = True,followers = followers,avatar = avatar)
    # when to update? maybe later.
    BilibiliVideo.create(bvid=bvid, visible=False, poster=u) # it must be new.


# grace period to be one day. that's long enough. or not?
# we still need some more experiment.

# check api doc for hint.
def checkRegisteredVideo(
    bvid: str,
    grace_period=datetime.timedelta(days=1),
    check_interval=datetime.timedelta(hours=1),
):  # maybe the video is not immediately visible after registration.
    # check if they are published or not.
    info = getVideoInfo(bvid)
    # you update that 'last_check' and compare it with 'checkin_date'
    # you can schedule check every hour. not all the time.
    # basically the same thing. but we do not delete these video till the time is too late, after check.


# seems bilibili can automatically categorize video.
# we just need to find out how?
def checkPublishedVideo(bvid: str):
    # if published, the video is taken down afterwards, we will delete it.
    # check if video is still visible or taken down.
    # if video is not visible then we delete this video from database.
    # v = video.Video(bvid=bvid)
    # print(info)
    # dict_keys(['bvid', 'aid', 'videos', 'tid', 'tname', 'copyright', 'pic', 'title', 'pubdate', 'ctime', 'desc', 'desc_v2', 'state', 'duration', 'forward', 'rights', 'owner', 'stat', 'dynamic', 'dimension', 'premiere', 'teenage_mode', 'is_chargeable_season', 'is_story', 'no_cache', 'subtitle', 'is_season_display', 'user_garb', 'honor_reply', 'like_icon'])
    #  'state': -4,
    # bad state! what is the meaning of this state?
    # normal; state -> 0
    bilibiliVideo = BilibiliVideo.get_or_none(bvid=bvid)
    if bilibiliVideo is not None:
        info = getVideoInfo(bvid) # getting shit? we need some normal video for test.
        state = info["state"]
        visible = state == 0
        if not visible:
            # remove that thing.
                bilibiliVideoIndex = BilibiliVideo.get_or_none(rowid=bilibiliVideo.id)
                bilibiliVideo.delete_instance()
                if bilibiliVideoIndex is not None:
                    # remove that thing.
                    bilibiliVideoIndex.delete_instance()
        else:
            bilibiliVideo.last_check = datetime.datetime.now()
            bilibiliVideo.visible=True
            bilibiliVideo.save()
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


def searchAndRegisterVideos(query:str,iterate: bool = False,page_start: int = 1,params={"duration": BSP.all.duration._10分钟以下}):
    results = searchVideos(query, iterate=iterate, page_start=page_start, params=params)
    db = getBilibiliVideoDatabaseAndCreateTables()
    for v in results:
        # print(v)
        # breakpoint()
        mid, author, upic = v["mid"], v["author"], v["upic"]
        bilibiliUser, _ = BilibiliUser.get_and_update_or_create(
            username=author, user_id=mid, avatar=upic
        )
        bilibiliVideo, _ = BilibiliVideo.get_and_update_or_create(
            bvid=v["bvid"],
            visible=True,  # are you sure?
            last_check=datetime.datetime.now(),  # well this is not tested. test it!
            poster=bilibiliUser,  # is it my account anyway?
            play=v["play"],
            pic=linkFixer(v["pic"]),
            length=videoDurationStringToSeconds(v["duration"]),
            review=v["review"],
            pubdate=v["pubdate"],
            favorites=v["favorites"],
        )
        bilibiliVideoIndex, _ = BilibiliVideoIndex.get_and_update_or_create(
            rowid=bilibiliVideo.id, description=v["description"], title=v["title"], tag=v['tag']
        )
        yield bilibiliVideoIndex, bilibiliVideo.bvid, bilibiliVideo.pic

if __name__ == "__main__":
    # test = 'searchVideos'
    test = 'searchUserVideos'
    # test = 'registerMyVideo'
    if test == 'searchUserVideos':
        query = '猫'
        for v in searchUserVideos(query):
            print('fetched value:',v)
            breakpoint()
    elif test == 'registerMyVideo':
        bvid = "BV1iw411Z7xt"
        dedeuserid = "397424026"
        registerMyVideo(bvid, dedeuserid)
    elif test == "searchVideos":
        query = "cod19"  # recent hot videos.
        # breakpoint()
        for v in searchAndRegisterVideos(query):
            print(v)
        # you want to select video after search?
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
