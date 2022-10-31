# from bindings import OPQBot
# from bindings_qzone import qzone
from bindings_all import qzone, OPQBot
QQ=917521610
serverPort = "8784"
OPQUrl = "http://localhost:"+serverPort
bot = OPQBot.NewBotManager(QQ, OPQUrl)
bot.Start()
# print(bot)
cookie = bot.GetUserCookie()
# print(cookie)
# you might want the cookie.
# <class 'bindings.OPQBot.Cookie'>
# qzone.OPQBot
qzoneManager = qzone.NewQzoneManager(QQ, cookie)
print(qzoneManager) # so far so good.
# result =
# it is not running. fuck.
content = 'hello world'
result = qzoneManager.SendShuoShuo(content)
print(result) # error to get qzone token. wtf?