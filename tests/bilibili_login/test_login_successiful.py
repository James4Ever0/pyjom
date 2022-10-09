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
dataList = db.search(User.dedeuserid == ) # this will never change i suppose?
if len(dataList)
credential = Credential()
from bilibili_api import sync
name = sync(get_self_info(credential))['name']
