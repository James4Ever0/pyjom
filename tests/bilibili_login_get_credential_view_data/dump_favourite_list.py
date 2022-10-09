from bilibili_api import favorite_list

# that favourite list is public. i just want that.
# dedeuserid = "397424026"
# how to?
from bilibili_api.user import get_self_info
from bilibili_api import sync, Credential

# how to load credential from our stored things?
# from bilibili_api import user
from lazero.search.api import getHomeDirectory
import os
import tinydb

home = getHomeDirectory()
dbPath = os.path.join(home, ".bilibili_api.json")
import tinydb

db = tinydb.TinyDB(dbPath)
dbFavList = tinydb.TinyDB("bilibiliFavouriteList.json")
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
    # now you have it.
    result = sync(
        favorite_list.get_video_favorite_list(int(dedeuserid), None, credential)
    )
    print(result)  # None? wtf?
    favLists = result["list"]
    for favList in favLists:
        listId = favList["id"]  # integer.
        listName = favList["title"]
        print("processing favList:", listName)
        page = 0
        while True:
            import time

            time.sleep(3)
            page += 1
            print("processing page:", page)
            result = sync(
                favorite_list.get_video_favorite_list_content(
                    listId, page=page, credential=credential
                )
            )
            # import pprint
            # pprint.pprint(result)
            has_more = result["has_more"]
            # print("__________result__________")
            medias = result["medias"]
            if type(medias) != list or len(medias) == 0:
                break
            breakFlag = False
            for elem in medias:
                # print('ELEM:',elem)
                # breakpoint()
                # it has description.
                videoData = {key: elem[key] for key in ["bvid", "title"]}
                # here we call 'desc' as 'intro.
                videoData.update({"desc": elem["intro"]})
                searchResult= dbFavList.search(User.bvid == videoData["bvid"])
                if len(searchResult) != 0:
                    breakFlag=True
                dbFavList.upsert(videoData, User.bvid == videoData["bvid"])
            if not has_more or breakFlag:
                break
