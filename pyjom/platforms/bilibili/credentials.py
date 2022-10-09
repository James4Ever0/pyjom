# you need to manage login/logout and credential storage.
# first you need to get 'home' directory
from lazero.search.api import getHomeDirectory
import os
from bilibili_api import sync, Credential
from bilibili_api.user import get_self_info
from bilibili_api import settings
from bilibili_api.login import (
    # login_with_password,
    login_with_sms,
    send_sms,
    PhoneNumber,
    # Check,
)

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
            db.upsert(
        {
            "name": credential.name,
            "dedeuserid": credential.dedeuserid,
            "bili_jct": credential.bili_jct,
            "buvid3": credential.buvid3,
            "sessdata": credential.sessdata,
        },
        User.dedeuserid == credential.dedeuserid,
    )
            return name
        else:
            return True
    except:
        import traceback
        traceback.print_exc()
        print('invalid credential:', credential)
        return False

def removeCredentialByDedeUserId(dedeuserid):
    try:
        db.remove(User.dedeuserid == dedeuserid)
        return True
    except:
        import traceback
        traceback.print_exc()
        print('error when removing credential from database for dedeuserid:', dedeuserid)
        return False


def getCredentialByDedeUserId(dedeuserid:str="397424026"):
    dataList = db.search(User.dedeuserid == dedeuserid)
    if len(dataList) !=1:
        if len(dataList) != 0:
            # remove all related records.
            print('multiple credentials found for dedeuserid:', dedeuserid)
            removeCredentialByDedeUserId(dedeuserid)
        else:
            print('no credential found for dedeuserid:', dedeuserid)
    else:
        # check validity.
        data = dataList[0].copy()
        print("try to login credential fetched from db:", data)
        oldName = data.pop("name")
        credential = Credential(**data)
        name = verifyCredential(credential)
        if name != False:
            print("login successful:", name)
            return credential
        else:
            print("login failed with existing credential for user:", oldName)
            removeCredentialByDedeUserId(dedeuserid)
    # anyway if you are here, nothing in database related to this dedeuserid now.
    # you choose to login via SMS.
    while True:
        phone = input("请输入手机号：")
        print("正在登录。")
        send_sms(PhoneNumber(phone, country="+86"))  # 默认设置地区为中国大陆
        code = input("请输入验证码：")
        c = login_with_sms(PhoneNumber(phone, country="+86"), code)
        credential = c
        # first, check if this is a valid credential.
        name = verifyCredential(credential)
        if name != False:
            print("登录成功")
            # update with this credential!
            # next, check if this is the credential we need.
            if credential.dedeuserid == dedeuserid:
                return credential
            else:
                print('dedeuserid not right.')
                print('user %s ')
        else:
            print('登陆失败')