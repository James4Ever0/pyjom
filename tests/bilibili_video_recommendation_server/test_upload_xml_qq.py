from botoy import Action

qq = 917521610
port = 8784
action = Action(qq=qq, port=port, host="127.0.0.1")
user = 1281727431
# but the goddamn xml format is not right.
# cover = "http://inews.gtimg.com/newsapp_bt/0/15352117085/640"
cover = "http://pubminishare-30161.picsz.qpic.cn/d4ad36fa-833e-4018-b994-a2da810f2d54"
# just need a better cover. i don't know.
# cover = "https://i0.hdslb.com/bfs/archive/c5a0d18ee077fb6a4ac0970ccb0a3788e137d14f.jpg" # works.
# content = """<?xml version='1.0' encoding='UTF-8' standalone='yes'?><msg templateID="123" url="https://b23.tv/5K7qh7K?share_medium=android&amp;share_source=qq&amp;bbid=XY46C7C4C74C8D645671EF7E8F4CC7810054A&amp;ts=1657521142233" serviceID="1" action="web" actionData="" a_actionData="" i_actionData="" brief="[QQ小程序]哔哩哔哩" flag="0"><item layout="2"><picture cover="{}"/><title>哔哩哔哩</title><summary>【C语言】《带你学C带你飞》</summary></item><source url="https://b23.tv/5K7qh7K?share_medium=android&amp;share_source=qq&amp;bbid=XY46C7C4C74C8D645671EF7E8F4CC7810054A&amp;ts=1657521142233" icon="https://open.gtimg.cn/open/app_icon/00/95/17/76/100951776_100_m.png?t=1657091104" name="哔哩哔哩" appid="0" action="web" actionData="" a_actionData="tencent0://" i_actionData=""/></msg>""".format(
    # cover
# )
# content = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?><msg templateID="123" url="https://b23.tv/uHML5mi?share_medium=android&amp;share_source=qq&amp;bbid=XY1BB721B1F97348DBDE4297FE1B4ABE26BAA&amp;ts=1666023406285" serviceID="1" action="web" actionData="" a_actionData="" i_actionData="" brief="[QQ小程序]哔哩哔哩" flag="0"><item layout="2"><picture cover="{}"/><title>【AI动画】妮露PV动画 风转换【NovelAI】</title></item><source url="https://b23.tv/uHML5mi?share_medium=android&amp;share_source=qq&amp;bbid=XY1BB721B1F97348DBDE4297FE1B4ABE26BAA&amp;ts=1666023406285" icon="http://miniapp.gtimg.cn/public/appicon/432b76be3a548fc128acaa6c1ec90131_200.jpg" name="哔哩哔哩" appid="0" action="app" actionData="" a_actionData="tencent0://" i_actionData=""/></msg>""".format(cover)
# i guess, it is just the way it send the data is different.
# result= action.sendFriendXml(user=user, content=content)
# print(result)

# content="""{"app":"com.tencent.gamecenter.gameshare","desc":"","view":"singleImg","ver":"0.0.0.0","prompt":"邪少QQXML论坛","appID":"","sourceName":"","actionData":"","actionData_A":"","sourceUrl":"","meta":{"singleImg":{"mainImage":"https://gchat.qpic.cn/gchatpic_new/3020005669/916530575-2949639428-6E45D21EADE33511C565E25AB432AB59/0?term=2","mainUrl":""}},"config":{"forward":1},"text":"","sourceAd":""}"""
group = 543780931
# have error when sending group xml? why?
# result = action.sendGroupXml(group=group, content=content)
# successful!
# this 'com.tencent.structmsg' might be our way. just maybe.
content = """{"app":"com.tencent.structmsg","desc":"","view":"news","ver":"0.0.0.1","prompt":"邪少QQXML论坛","appID":100951776,"sourceName":"","actionData":"","actionData_A":"","sourceUrl":"","meta":{"singleImg":{"mainImage":"https://gchat.qpic.cn/gchatpic_new/3020005669/916530575-2949639428-6E45D21EADE33511C565E25AB432AB59/0?term=2","mainUrl":""}},"text":"","extraApps":[],"sourceAd":"","config":{"forward":1}}"""
# content = """{"app":"com.tencent.gamecenter.gameshare","desc":"","view":"singleImg","ver":"0.0.0.0","prompt":"邪少QQXML论坛","appID":"","sourceName":"","actionData":"","actionData_A":"","sourceUrl":"","meta":{"singleImg":{"mainImage":"https://gchat.qpic.cn/gchatpic_new/3020005669/916530575-2949639428-6E45D21EADE33511C565E25AB432AB59/0?term=2","mainUrl":""}},"text":"","extraApps":[],"sourceAd":"","config":{"forward":1}}"""
# content = """<?xml version='1.0' encoding='UTF-8' standalone='yes' ?><msg templateID="123" url="https://b23.tv/uHML5mi?share_medium=android&amp;share_source=qq&amp;bbid=XY1BB721B1F97348DBDE4297FE1B4ABE26BAA&amp;ts=1666023406285" serviceID="1" action="web" actionData="" a_actionData="" i_actionData="" brief="[QQ小程序]哔哩哔哩" flag="0"></msg>"""
result = action.sendGroupJson(group=group, content=content)
# result = action.sendGroupXml(group=group, content=content)
print(result)
# result = action.sendGroupText(group=group,content='test')
# result = action.sendGroupText(group=group,content=content)
# funcname = "SendMsgV2"
# content = """<?xml version='1.0' encoding='UTF-8' standalone='yes' ?><msg serviceID='1' templateID='1' action='' brief='&#91;群僵尸任务&#93;' sourceMsgId='0' url='' flag='2' adverSign='0' multiMsgFlag='0'><item layout='0'><title size='38' color='#9900CC' style='1'>🆕已经启动🆕</title></item><item layout='0'><hr hidden='false' style='0' /></item><item layout='6'><summary color='#FF0033'>1⃣️</summary><summary color='#FF0099'>💪正在扫秒僵尸💪</summary></item><source name='' icon='' action='' appid='-1' /></msg>"""
# content = """<?xml version='1.0' encoding='UTF-8' standalone='yes' ?><msg serviceID="2" templateID="1" action="web" brief="&#91;分享&#93; 十年" sourceMsgId="0" url="https://i.y.qq.com/v8/playsong.html?_wv=1&amp;songid=4830342&amp;souce=qqshare&amp;source=qqshare&amp;ADTAG=qqshare" flag="0" adverSign="0" multiMsgFlag="0" ><item layout="2"><audio cover="http://imgcache.qq.com/music/photo/album_500/26/500_albumpic_89526_0.jpg" src="http://ws.stream.qqmusic.qq.com/C400003mAan70zUy5O.m4a?guid=1535153710&amp;vkey=D5315B8C0603653592AD4879A8A3742177F59D582A7A86546E24DD7F282C3ACF81526C76E293E57EA1E42CF19881C561275D919233333ADE&amp;uin=&amp;fromtag=3" /><title>十年</title><summary>陈奕迅</summary></item><source name="QQ音乐" icon="https://i.gtimg.cn/open/app_icon/01/07/98/56/1101079856_100_m.png" url="http://web.p.qq.com/qqmpmobile/aio/app.html?id=1101079856" action="app"  a_actionData="com.tencent.qqmusic" i_actionData="tencent1101079856://" appid="1101079856" /></msg>"""
# content = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?><msg serviceID="1" templateID="1" action="" brief="QQ红包" sourceMsgId="0" flag="8" adverSign="0" multiMsgFlag="0"><item layout="6"><title color="#EE00EE" style="4">阿深真帅</title><summary color="#9A32CD">是不是很无语</summary><picture cover="http://t1.hddhhn.com/uploads/tu/20150507/20405-eBE9jO.jpg" action="web" url="http://url.cn/5g4eOiY" w="0" h="0"/></item></msg>"""
# payload = {
#     "ToUserUid": group,
#     "SendToType": 2,
#     "SendMsgType": "XmlMsg",
#     "Content": content,
# }
# result = action.baseRequest(
#     method="POST",
#     funcname=funcname,
#     path="/v1/LuaApiCaller",
#     params={"qq": qq, "funcname": funcname},
#     payload=payload,
# )
# print(result)
