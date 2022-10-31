from bindings import OPQBot

QQ=917521610
serverPort = "8784"
OPQUrl = "http://localhost:"+serverPort
bot = OPQBot.NewBotManager(QQ, OPQUrl)
bot.Start()
print(bot)
# it is not running. fuck.