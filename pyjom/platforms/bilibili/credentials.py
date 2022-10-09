# you need to manage login/logout and credential storage.
# first you need to get 'home' directory
from lazero.search.api import getHomeDirectory
import os
from bilibili_api import sync
from bilibili_api.user import get_self_info


home = getHomeDirectory()
dbPath = os.path.join(home, ".bilibili_api.json")
import tinydb

db = tinydb.TinyDB(dbPath) # is this variable shared in this module?
User = tinydb.Query()

def verifyCredentialAndGetName(credential):
    try:
        name = sync(get_self_info(credential))["name"]
        print('credential valid for:', name)
        return name


def getCredentialByDedeUserId(dedeuserid):
    dataList = db.search(User.dedeuserid == dedeuserid)