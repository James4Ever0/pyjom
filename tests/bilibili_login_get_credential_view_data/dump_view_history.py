# how to?
from bilibili_api.user import get_self_info
from bilibili_api import Credential

# how to load credential from our stored things?
from bilibili_api import user
from lazero.search.api import getHomeDirectory
import os
import tinydb

home = getHomeDirectory()
dbPath = os.path.join(home, ".bilibili_api.json")
import tinydb

db = tinydb.TinyDB(dbPath)
User = tinydb.Query()
dedeuserid = "397424026"  # pass it before you do shit!
dataList = db.search(User.dedeuserid == dedeuserid)  # this will never change i suppose?
if len(dataList) == 1:
    data = dataList[0].copy()
    print("try to login credential fetched from db:", data)
    oldName = data.pop("name")
    credential = Credential(**data)
    from bilibili_api import sync

    name = sync(get_self_info(credential))["name"]
    if oldName != name:
        data["name"] = name
        db.upsert(data, User.dedeuserid == dedeuserid)
    print("login successful:", name)
    # now continue.
    # how many pages you want? infinite?
    import time

    page_num = 0
    dbHistory = tinydb.TinyDB("bilibiliHistory.json")
    while True:
        time.sleep(3)
        page_num += 1  # starts with 1
        print("now processing page:", page_num)
        result = sync(
            user.get_self_history(
                page_num=page_num, per_page_item=100, credential=credential
            )
        )
        # import pprint
        # pprint.pprint(result)
        if type(result) != list or len(result) == 0:
            break
        breakFlag=False
        for elem in result:
            # it has description.
            videoData = {key: elem[key] for key in ["bvid", "desc", "title"]}
            searchResult= dbHistory.search(User.bvid == videoData["bvid"])
            if len(searchResult) != 0:
                breakFlag=True
            dbHistory.upsert(videoData, User.bvid == videoData["bvid"])
        if breakFlag:
            break
