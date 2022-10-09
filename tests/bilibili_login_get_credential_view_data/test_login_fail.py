from bilibili_api.user import get_self_info
from bilibili_api import Credential
# how to load credential from our stored things?

from lazero.search.api import getHomeDirectory
import os
import tinydb

home = getHomeDirectory()
dbPath = os.path.join(home, ".bilibili_api.json")
import tinydb
db = tinydb.TinyDB(dbPath)
User = tinydb.Query()
dedeuserid = "397424026" # pass it before you do shit!
dataList = db.search(User.dedeuserid == dedeuserid) # this will never change i suppose?
if len(dataList) == 1:
    data = dataList[0].copy()
    print('try to login credential fetched from db:', data)
    oldName = data.pop('name')
    credential = Credential(**{'dedeuserid': dedeuserid,'sessdata':'fakeSessionData'})
    from bilibili_api import sync
    name = sync(get_self_info(credential))['name']
    # 'GetCookieReq.Session' Error:Field validation for 'Session' failed on the 'gte' tag。
    # don't know how. maybe this works?
    # if oldName !=name:
    #     data['name']=name
    #     db.upsert(data, User.dedeuserid == dedeuserid)
    # will never succeed.
    # don't know using some expired sessdata will get what?
    # maybe will still fail?
    print('login successful:', name)
