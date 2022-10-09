from bilibili_api.login import (
    login_with_password,
    login_with_sms,
    send_sms,
    PhoneNumber,
    Check,
)
from bilibili_api.user import get_self_info
from bilibili_api import settings
from bilibili_api import sync, Credential

# mode = int(input("""请选择登录方式：
# 1. 密码登录
# 2. 验证码登录
# 请输入 1/2
# """))
mode = 2

credential = None

# 关闭自动打开 geetest 验证窗口
settings.geetest_auto_open = False

if mode == 1:
    # 密码登录
    username = input("请输入手机号/邮箱：")
    password = input("请输入密码：")
    print("正在登录。")
    c = login_with_password(username, password)
    if isinstance(c, Check):
        # 还需验证
        phone = input("需要验证。请输入手机号：")
        c.set_phone(PhoneNumber(phone, country="+86"))  # 默认设置地区为中国大陆
        c.send_code()
        print("已发送验证码。")
        code = input("请输入验证码：")
        credential = c.login(code)
        print("登录成功！")
    else:
        credential = c
elif mode == 2:
    # 验证码登录
    phone = input("请输入手机号：")
    print("正在登录。")
    send_sms(PhoneNumber(phone, country="+86"))  # 默认设置地区为中国大陆
    code = input("请输入验证码：")
    c = login_with_sms(PhoneNumber(phone, country="+86"), code)
    credential = c
    print("登录成功")
else:
    print("请输入 1/2 ！")
    exit()

from lazero.search.api import getHomeDirectory
import os

home = getHomeDirectory()
dbPath = os.path.join(home, ".bilibili_api.json")
import tinydb

db = tinydb.TinyDB(dbPath)
if credential != None:
    name = sync(get_self_info(credential))["name"]
    print(f"欢迎，{name}!")
    buvid3 = credential.buvid3
    bili_jct = credential.bili_jct
    sessdata = credential.sessdata
    dedeuserid = credential.dedeuserid  # this is userid, better use this instead?
    User = tinydb.Query()
    # assume that we are here to fetch valid credentials.
    db.upsert(
        {
            "name": name,
            "dedeuserid": dedeuserid,
            "bili_jct": bili_jct,
            "buvid3": buvid3,
            "sessdata": sessdata,
        },
        User.dedeuserid == dedeuserid,
    )
    # how to perform atomic insert in tinydb?
    # breakpoint()
