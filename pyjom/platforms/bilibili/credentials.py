# you need to manage login/logout and credential storage.
# first you need to get 'home' directory
from lazero.search.api import getHomeDirectory
import os
from bilibili_api import sync, Credential
from bilibili_api.user import get_self_info
from bilibili_api import settings

settings.geetest_auto_open = False


home = getHomeDirectory()
dbPath = os.path.join(home, ".bilibili_api.json")
import tinydb

db = tinydb.TinyDB(dbPath) # is this variable shared in this module?
User = tinydb.Query()

def verifyCredential(credential,returnName=True):
    try:
        name = sync(get_self_info(credential))["name"]
        print('credential valid for:', name)
        if returnName:
            return name
        else:
            return True
    except:
        import traceback
        traceback.print_exc()
        print('invalid credential:', credential)
        return False


def getCredentialByDedeUserId(dedeuserid):
    dataList = db.search(User.dedeuserid == dedeuserid)
    if len(dataList) !=1:
        if len(dataList) != 0:
            # remove all related records.
            db.remove(User.dedeuserid == dedeuserid)
    else:
        # check validity.
        data = dataList[0].copy()
        print("try to login credential fetched from db:", data)
        oldName = data.pop("name")
        credential = Credential(**data)
        name = verifyCredential(credential)
        if name != False:
            if oldName != name:
                data["name"] = name
                db.upsert(data, User.dedeuserid == dedeuserid)
            print("login successful:", name)
        else:
            print("login failed: