from bindings import OPQBot
from bindings_qzone import qzone
QQ=917521610
serverPort = "8784"
OPQUrl = "http://localhost:"+serverPort
bot = OPQBot.NewBotManager(QQ, OPQUrl)
bot.Start()
# print(bot)
cookie = bot.GetUserCookie()
# print(cookie, type(cookie))
# <class 'bindings.OPQBot.Cookie'>
qzoneManager = qzone.NewQzoneManager(QQ, cookie)

# result =
# it is not running. fuck.