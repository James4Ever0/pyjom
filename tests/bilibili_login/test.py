from bilibili_api import login, user, sync

while True:
    print("请登录：")
    credential = login.login_with_qrcode()  # what are you doing here?
    # this is some GUI function. no terminal support!
    try:
        credential.raise_for_no_bili_jct()  # 判断是否成功
        credential.raise_for_no_sessdata()  # 判断是否成功
        credential.raise_for_no_buvid3()
        credential.raise_for_no_dedeuserid()
        break
    except:
        print("登陆失败。。。")
    # exit()
    # do not exit! retry!
userName = sync(user.get_self_info(credential))["name"]
print("欢迎，", userName, "!")
# dict(credential)
buvid3 = credential.buvid3
bili_jct = credential.bili_jct
sessdata = credential.sessdata
userId = credential.dedeuserid  # this is userid, better use this instead?
breakpoint()
# check validity of my credentials?

