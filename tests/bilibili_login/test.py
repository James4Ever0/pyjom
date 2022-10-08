from bilibili_api import login, user, sync
print("请登录：")
credential = login.login_with_qrcode() # what are you doing here?
# this is some GUI function. no terminal support!
try:
    credential.raise_for_no_bili_jct() # 判断是否成功
    credential.raise_for_no_sessdata() # 判断是否成功
except:
    print("登陆失败。。。")
    exit()
print("欢迎，", sync(user.get_self_info(credential))['name'], "!")
credential.buvid3
credential.