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
dedeuserid = # pass it before you do shit!
dataList = db.search(User.dedeuserid == dedeuserid) # this will never change i suppose?
if len(dataList) == 1:
    data = dataList[0].copy()
    oldName = data[0]['name']
    credential = Credential()
    from bilibili_api import sync
    name = sync(get_self_info(credential))['name']
    if oldName !=name:
        data['name']=name
        db.upsert(data, User.dedeuserid == dedeuserid)
    
