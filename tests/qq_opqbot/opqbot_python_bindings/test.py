from bindings import OPQBot
from bindings_qzone import qzone
QQ=917521610
serverPort = "8784"
OPQUrl = "http://localhost:"+serverPort
bot = OPQBot.NewBotManager(QQ, OPQUrl)
bot.Start()
print(bot)
# result =
# it is not running. fuck.