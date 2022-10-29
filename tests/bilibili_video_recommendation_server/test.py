# serve my video, serve my cat video, dog video, set priority, serve others video
# by means of query? or just directly ask me for it.

# you'd better mimic the video that you have never recommend, and these audience have never seen before.
import time
import sys
import datetime
from typing import Union
from functools import lru_cache

sys.path.append("/root/Desktop/works/pyjom/")
# you might want to add this to bilibili platform api, if there's no use of pyjom.commons
from pyjom.platforms.bilibili.credentials import getCredentialByDedeUserId
from pyjom.platforms.bilibili.utils import linkFixer, videoDurationStringToSeconds

from lazero.search.preprocessing import getFourVersionsOfProcessedLine
import jieba
import opencc


@lru_cache(maxsize=4)
def getOpenCCConverter(converter_type: str = "t2s"):
    converter = opencc.OpenCC(converter_type)
    return converter


def isChineseCharacter(char):
    assert len(char) == 1
    return char >= "\u4e00" and char <= "\u9fff"


def containChineseCharacters(text):
    for char in text:
        if isChineseCharacter(char):
            return True
    return False


from lazero.utils.mathlib import extract_span


def textPreprocessing(text):
    converter = getOpenCCConverter()
    text = converter.convert(text)
    (
        final_line,
        final_cutted_line,
        final_stemmed_line,
        final_cutted_stemmed_line,
    ) = getFourVersionsOfProcessedLine(text)
    # breakpoint()
    wordlist = jieba.lcut(final_cutted_line)
    final_wordlist = []
    for w in wordlist:
        word = w.strip()
        if len(word) > 0:
            final_wordlist.append(word)
    flags = [int(containChineseCharacters(word)) for word in final_wordlist]
    chineseSpans = extract_span(flags, target=1)
    nonChineseSpans = extract_span(flags, target=0)
    finalSpans = [(span, True) for span in chineseSpans] + [
        (span, False) for span in nonChineseSpans
    ]
    finalSpans.sort(key=lambda span: span[0])
    finalWordList = []
    for span, isChineseSpan in finalSpans:
        subWordList = final_wordlist[span[0] : span[1]]
        if isChineseSpan:
            subWordList = jieba.lcut_for_search("".join(subWordList))
        finalWordList.extend(subWordList)
    return " ".join(finalWordList)


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


@lru_cache(maxsize=1)
def getMajorMinorTopicMappings(debug: bool = False):
    majorMinorMappings = {}
    for key, value in BSP.all.tids.__dict__.items():
        try:
            major_tid = value.tid
            if debug:
                print("MAJOR", key, major_tid)
            content = {"major": {"tid": major_tid, "name": key}}
            majorMinorMappings.update(
                {major_tid: content, key: content, str(major_tid): content}
            )
            for subkey, subvalue in value.__dict__.items():
                if subkey != "tid" and type(subvalue) == int:
                    if debug:
                        print("MINOR", subkey, subvalue)
                    content = {
                        "major": {"tid": major_tid, "name": key},
                        "minor": {"tid": subvalue, "name": subkey},
                    }
                    majorMinorMappings.update(
                        {subvalue: content, subkey: content, str(subvalue): content}
                    )
        except:
            pass
    return majorMinorMappings


def getTagStringFromTid(tid):
    majorMinorTopicMappings = getMajorMinorTopicMappings()
    topic = majorMinorTopicMappings.get(tid, None)
    tags = []
    if topic:
        majorTopic = topic.get("major", {}).get("name", None)
        minorTopic = topic.get("minor", {}).get("name", None)
        if majorTopic:
            tags.append(majorTopic)
            if minorTopic:
                tags.append(minorTopic)
    return ",".join(tags)


# also make a decorator for refreshing status, add it to every function.
# thie refresher is scheduled.
# you may want to run this beforehand...

import schedule

# do we really need credential for checking our video? you can try.


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
    user_id = IntegerField(unique=True)  # this is integer.
    is_mine = BooleanField(default=False)
    followers = IntegerField(
        null=True
    )  # how to get that? every time you get some video you do this shit? will get you blocked.
    # well you can check it later.
    avatar = CharField(null=True)  # warning! charfield max length is 255


class BilibiliVideo(Model):
    bvid = CharField(unique=True)
    typeid = IntegerField(null=True)
    visible = BooleanField(null=True)  # are you sure?
    last_check = DateTimeField(
        default=datetime.datetime.now
    )  # well this is not tested. test it!
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
    title = CharField(null=True)
    tag = CharField(null=True)
    description = CharField(null=True)


class BilibiliVideoIndex(FTSModel):
    rowid = RowIDField()
    # these three must be preprocessed before put into the search engine, or we cannot retrieve the data correctly.
    title = SearchField()
    tag = (
        SearchField()
    )  # also what the fuck is going on with the tag? why we cannot get the tag/topic name?
    description = SearchField()

    class Meta:
        database = None  # that's good.
        options = {"tokenize": "porter"}  # you need manually separate some


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


# no need to decorate this thing. only put some 'unchecked' video into array.
def registerUser(dedeuserid: str, is_mine: Union[bool, None] = None):
    user_id = int(dedeuserid)
    u = BilibiliUser.get_or_none(user_id=user_id)
    if u is None:
        if is_mine is None:
            is_mine = False
        userObject = user.User(user_id)
        userInfo = sync(userObject.get_user_info())
        # print(userInfo)
        # print(dir(userInfo))
        # breakpoint()
        # dict_keys(['list', 're_version', 'total'])
        # in the 'list' we've got a few recent followers.
        followersInfo = sync(userObject.get_followers())
        username = userInfo["name"]
        followers = followersInfo["total"]
        avatar = userInfo["face"]
        u, _ = BilibiliUser.get_or_create(
            user_id=user_id,
            username=username,
            is_mine=is_mine,
            followers=followers,
            avatar=avatar,
        )
        # when to update? maybe later.
    elif is_mine is not None and u.is_mine != is_mine:
        u.is_mine = is_mine
        u.save()
    return u


# @refresh_status_decorator
def searchVideos(
    query: str,
    iterate: bool = False,
    page_start: int = 1,
    params={"duration": BSP.all.duration._10分钟以下},  # is that right? maybe?
):  # what do you expect? you want the xml object let's get it!
    # search the thing directly? or you distill keywords from it?
    search_type = search.SearchObjectType.VIDEO
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
    sleep: int = 2,
):  # all videos? just at init.
    # some stop condition for early termination.
    # if any of the video exists in the database, we stop this shit.
    bilibiliUser = registerUser(
        dedeuserid,
    )
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
        videos = sync(u.get_videos(pn=pn, keyword=keyword, tid=tid, order=order))
        # print(videos)
        # dict_keys(['list', 'page', 'episodic_button', 'is_risk', 'gaia_res_type', 'gaia_data'])
        page = videos["page"]  # pagination options
        numPages = math.ceil(page["count"] / page["ps"])
        # print('NUM PAGES',numPages)
        topicDict = videos["list"]["tlist"]
        # {'1': {'tid': 1, 'count': 13, 'name': '动画'}, '160': {'tid': 160, 'count': 257, 'name': '生活'}, '181': {'tid': 181, 'count': 2, 'name': '影视'}, '188': {'tid': 188, 'count': 4, 'name': '科技'}, '217': {'tid': 217, 'count': 4, 'name': '动物圈'}, '234': {'tid': 234, 'count': 1, 'name': '运动'}, '3': {'tid': 3, 'count': 9, 'name': '音乐'}, '36': {'tid': 36, 'count': 30, 'name': '知识'}, '4': {'tid': 4, 'count': 67, 'name': '游戏'}}
        # breakpoint()
        video_list = videos["list"]["vlist"]
        # breakpoint()
        if video_list == []:
            break
        for v in video_list:
            bvid = v["bvid"]
            subTypeId = v["typeid"]
            tagString = getTagStringFromTid(subTypeId)
            result = checkVideoInDatabase(bvid)
            if result and stop_on_duplicate:
                stopped = True
                break
            # print(v)
            # dict_keys(['comment', 'typeid', 'play', 'pic', 'subtitle', 'description', 'copyright', 'title', 'review', 'author', 'mid', 'created', 'length', 'video_review', 'aid', 'bvid', 'hide_click', 'is_pay', 'is_union_video', 'is_steins_gate', 'is_live_playback'])
            # breakpoint()
            # bad idea. you should get the bilibiliUser before you do this.
            bilibiliVideo, _ = BilibiliVideo.get_and_update_or_create(
                bvid=v["bvid"],
                typeid=v["typeid"],
                visible=True,  # are you sure?
                last_check=datetime.datetime.now(),  # well this is not tested. test it!
                poster=bilibiliUser,  # is it my account anyway?
                play=v["play"],
                pic=linkFixer(v["pic"]),
                length=videoDurationStringToSeconds(v["length"]),
                review=v["comment"],
                pubdate=v["created"],
                description=v["description"],
                title=v["title"],
                tag=tagString,
            )
            bilibiliVideoIndex, _ = BilibiliVideoIndex.get_and_update_or_create(
                rowid=bilibiliVideo.id,
                description=textPreprocessing(bilibiliVideo.description),
                tag=textPreprocessing(bilibiliVideo.tag),
                title=textPreprocessing(bilibiliVideo.title),
            )
            yield bilibiliVideo
        # videos['list']['vlist'][0].keys()
        # dict_keys(['comment', 'typeid', 'play', 'pic', 'subtitle', 'description', 'copyright', 'title', 'review', 'author', 'mid', 'created', 'length', 'video_review', 'aid', 'bvid', 'hide_click', 'is_pay', 'is_union_video', 'is_steins_gate', 'is_live_playback'])
        if pn >= numPages:
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
        order = None
        for v in getUserVideos(
            tid=tid,
            order=videoOrder,
            keyword=keyword,
            dedeuserid=dedeuserid,
            use_credential=use_credential,
            stop_on_duplicate=False,
        ):
            # what is the content? plan to update?
            # print("SEARCHED USER VIDEO ID:", v_id)
            resultList.append((v, order))
        # info = u.get_videos(keyword=keyword,order=videoOrder)
    elif method == "bm25":
        # export all video? shit?
        # you should tokenize the thing.
        # but this search does not have limitations!
        poster = registerUser(dedeuserid)
        user_video_ids = [
            v.id
            for v in BilibiliVideo.select(BilibiliVideo.id).where(
                BilibiliVideo.poster == poster
            )
        ]
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
            resultList.append((bilibiliVideo, order))
        resultList.sort(key=lambda x: x[1])
    for v, _ in resultList:
        yield v  # this is bilibiliVideoIndex, but you also needs the bvid.


# you can make excerpt from video to lure people into viewing your video.


def getVideoInfo(bvid: str):
    v = video.Video(bvid=bvid)
    info = sync(v.get_info())
    return info


def registerUserVideo(
    bvid: str, dedeuserid: str, is_mine: bool = False
):  # this is the video i just post. must be regularly checked then add to candidate list. you can check it when another call for my videos has been issued.
    # register user first, then register the video.
    # you will store it to database.
    u = registerUser(dedeuserid, is_mine)
    BilibiliVideo.create(bvid=bvid, visible=False, poster=u)  # it must be new.


# grace period to be one day. that's long enough. or not?
# we still need some more experiment.


def checkVideoVisibility(bvid: str):
    info = getVideoInfo(bvid)  # getting shit? we need some normal video for test.
    state = info["state"]
    visible = state == 0
    return visible


# check api doc for hint.
def checkRegisteredVideo(
    bvid: str,
    grace_period=datetime.timedelta(days=1),
    check_interval=datetime.timedelta(hours=1),
):  # maybe the video is not immediately visible after registration.
    # check if they are published or not.
    # ____CI____CI____CI____ (before check video info. decide to check or not.)
    # __________GP__________ (after check video info. decide to delete or not.)
    published = False
    bilibiliVideo = BilibiliVideo.get_or_none(bvid=bvid)
    now = datetime.datetime.now()
    needCheck = False
    if bilibiliVideo:
        visible = bilibiliVideo.visible
        needCheck = now - bilibiliVideo.last_check >= check_interval
        needRemove = now - bilibiliVideo.register_date >= grace_period
        if (
            visible and needRemove
        ):  # do not remove. it just need to be check again, when using checkPublishedVideo. this value is used for double check.
            published = True
        else:
            if needCheck:
                visible = checkVideoVisibility(bvid)
                if visible:
                    published = True
                elif needRemove:
                    bilibiliVideo.delete_instance()
    # you update that 'last_check' and compare it with 'checkin_date'
    # you can schedule check every hour. not all the time.
    # basically the same thing. but we do not delete these video till the time is too late, after check.
    return published, not needCheck


# seems bilibili can automatically categorize video.
# we just need to find out how?
def checkPublishedVideo(bvid: str):  # this is only done during retrieval.
    # if published, the video is taken down afterwards, we will delete it.
    # check if video is still visible or taken down.
    # if video is not visible then we delete this video from database.
    # v = video.Video(bvid=bvid)
    # print(info)
    # dict_keys(['bvid', 'aid', 'videos', 'tid', 'tname', 'copyright', 'pic', 'title', 'pubdate', 'ctime', 'desc', 'desc_v2', 'state', 'duration', 'forward', 'rights', 'owner', 'stat', 'dynamic', 'dimension', 'premiere', 'teenage_mode', 'is_chargeable_season', 'is_story', 'no_cache', 'subtitle', 'is_season_display', 'user_garb', 'honor_reply', 'like_icon'])
    #  'state': -4,
    # bad state! what is the meaning of this state?
    # normal; state -> 0
    avaliable = False
    bilibiliVideo = BilibiliVideo.get_or_none(bvid=bvid)
    if (
        bilibiliVideo is not None
    ):  # might be our 'registered' video but not yet been published.
        published, needCheckAgain = checkRegisteredVideo(bvid)
        if published:
            if not needCheckAgain:
                published = True
            else:
                visible = checkVideoVisibility(bvid)
                avaliable = visible
                if not visible:
                    # remove that thing.
                    bilibiliVideoIndex = BilibiliVideo.get_or_none(
                        rowid=bilibiliVideo.id
                    )
                    bilibiliVideo.delete_instance()
                    if bilibiliVideoIndex is not None:
                        # remove that thing.
                        bilibiliVideoIndex.delete_instance()
                else:
                    bilibiliVideo.last_check = datetime.datetime.now()
                    bilibiliVideo.visible = True
                    bilibiliVideo.save()
    else:
        print("video %s is not registered." % bvid)
    # info['stat'].keys()
    # dict_keys(['aid', 'view', 'danmaku', 'reply', 'favorite', 'coin', 'share', 'now_rank', 'his_rank', 'like', 'dislike', 'evaluation', 'argue_msg'])
    # breakpoint()
    # if anything goes wrong, do not return the state.
    # if you want update, better do it here. we are checking and updating the video.
    # we use some random video for test.
    return avaliable


# i suggest you to use sqlalchemy. since this is no ordinary task.
# you cannot just check every video of your own in the past.

## following code is for test purpose.

# shall write some server.
# not fastapi!


def searchAndRegisterVideos(
    query: str,
    iterate: bool = False,
    page_start: int = 1,
    params={"duration": BSP.all.duration._10分钟以下},
):
    results = searchVideos(query, iterate=iterate, page_start=page_start, params=params)
    # db = getBilibiliVideoDatabaseAndCreateTables()
    # this database connection will be established elsewhere.
    for v in results:
        # print(v)
        # breakpoint()
        mid, author, upic = v["mid"], v["author"], v["upic"]
        bilibiliUser, _ = BilibiliUser.get_and_update_or_create(
            username=author, user_id=mid, avatar=linkFixer(upic)
        )
        bilibiliVideo, _ = BilibiliVideo.get_and_update_or_create(
            bvid=v["bvid"],
            typeid=v["typeid"],
            visible=True,  # are you sure?
            last_check=datetime.datetime.now(),  # well this is not tested. test it!
            poster=bilibiliUser,  # is it my account anyway?
            play=v["play"],
            pic=linkFixer(v["pic"]),
            length=videoDurationStringToSeconds(v["duration"]),
            review=v["review"],
            pubdate=v["pubdate"],
            favorites=v["favorites"],
            description=v["description"],
            title=v["title"],
            tag=v["tag"],
        )
        bilibiliVideoIndex, _ = BilibiliVideoIndex.get_and_update_or_create(
            rowid=bilibiliVideo.id,
            description=textPreprocessing(bilibiliVideo.description),
            tag=textPreprocessing(bilibiliVideo.tag),
            title=textPreprocessing(bilibiliVideo.title),
        )
        yield bilibiliVideo


def refresh_status(
    grace_period=datetime.timedelta(days=1),
    check_interval=datetime.timedelta(hours=1),
):
    # what to do? just select and update?
    # but you need the database object. it is loop dependency!
    # well we can split the function.
    # just for initialization?
    now_minus_check_period = datetime.datetime.now() - check_interval
    selector = BilibiliVideo.select(BilibiliVideo.bvid).where(
        BilibiliVideo.last_check < now_minus_check_period
    )  # need check or not?
    for bvid in selector:
        checkRegisteredVideo(
            bvid, grace_period=grace_period, check_interval=check_interval
        )
    return


def refresh_status_decorator(func):
    def wrapper(*args, **kwargs):
        schedule.run_pending()
        return func(*args, **kwargs)

    return wrapper


@refresh_status_decorator  # this might prevent you adding the decorator everywhere?
def getBilibiliVideoDatabaseCreateTablesAndRefreshStatus():
    db = getBilibiliVideoDatabaseAndCreateTables()
    return db


if __name__ == "__main__":
    db = getBilibiliVideoDatabaseAndCreateTables()
    refresh_status()  # ensure the database is connected.
    schedule.every(20).minutes.do(refresh_status)
    # test = 'searchVideos'
    # test = "searchUserVideos"
    test = "textPreprocessing"
    # test = 'registerMyVideo'
    if test == "textPreprocessing":
        text = "猫  咪  钢  琴  家 searchUserVideos have a nice day 新闻联播"
        result = textPreprocessing(text)
        print("RESULT:", result)
    elif test == "searchUserVideos":
        query = "猫"
        for v in searchUserVideos(query):
            print("fetched value:", v)
            breakpoint()
    elif test == "registerMyVideo":
        bvid = "BV1fR4y1w7BL"  # that's surely yours.
        dedeuserid = "397424026"
        registerUserVideo(bvid, dedeuserid)
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
