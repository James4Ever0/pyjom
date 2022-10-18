from botoy import Action

qq = 917521610
port = 8784
action = Action(qq=qq, port=port, host='127.0.0.1')
user=1281727431
# but the goddamn xml format is not right.
# cover = "http://inews.gtimg.com/newsapp_bt/0/15352117085/640"
cover = "http://pubminishare-30161.picsz.qpic.cn/d4ad36fa-833e-4018-b994-a2da810f2d54"
# just need a better cover. i don't know.
# cover = "https://i0.hdslb.com/bfs/archive/c5a0d18ee077fb6a4ac0970ccb0a3788e137d14f.jpg" # works.
content = """<?xml version='1.0' encoding='UTF-8' standalone='yes'?><msg templateID="123" url="https://b23.tv/5K7qh7K?share_medium=android&amp;share_source=qq&amp;bbid=XY46C7C4C74C8D645671EF7E8F4CC7810054A&amp;ts=1657521142233" serviceID="1" action="web" actionData="" a_actionData="" i_actionData="" brief="[QQ小程序]哔哩哔哩" flag="0"><item layout="2"><picture cover="{}"/><title>哔哩哔哩</title><summary>【C语言】《带你学C带你飞》</summary></item><source url="https://b23.tv/5K7qh7K?share_medium=android&amp;share_source=qq&amp;bbid=XY46C7C4C74C8D645671EF7E8F4CC7810054A&amp;ts=1657521142233" icon="https://open.gtimg.cn/open/app_icon/00/95/17/76/100951776_100_m.png?t=1657091104" name="哔哩哔哩" appid="0" action="web" actionData="" a_actionData="tencent0://" i_actionData=""/></msg>""".format(cover)
# content = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?><msg templateID="123" url="https://b23.tv/uHML5mi?share_medium=android&amp;share_source=qq&amp;bbid=XY1BB721B1F97348DBDE4297FE1B4ABE26BAA&amp;ts=1666023406285" serviceID="1" action="web" actionData="" a_actionData="" i_actionData="" brief="[QQ小程序]哔哩哔哩" flag="0"><item layout="2"><picture cover="{}"/><title>【AI动画】妮露PV动画 风转换【NovelAI】</title></item><source url="https://b23.tv/uHML5mi?share_medium=android&amp;share_source=qq&amp;bbid=XY1BB721B1F97348DBDE4297FE1B4ABE26BAA&amp;ts=1666023406285" icon="http://miniapp.gtimg.cn/public/appicon/432b76be3a548fc128acaa6c1ec90131_200.jpg" name="哔哩哔哩" appid="0" action="app" actionData="" a_actionData="tencent0://" i_actionData=""/></msg>""".format(cover)
# i guess, it is just the way it send the data is different.
# result= action.sendFriendXml(user=user, content=content)
# print(result)

# content="""{"app":"com.tencent.gamecenter.gameshare","desc":"","view":"noDataView","ver":"0.0.0.0","prompt":"邪少QQXML论坛","appID":"","sourceName":"","actionData":"","actionData_A":"","sourceUrl":"","meta":{"shareData":{"scene":"SCENE_SHARE_VIDEO","jumpUrl":"https://attachments-cdn.shimo.im/ozL6gi2dwLpsUdA9.mp4","type":"video","url":"https://t.cn/A6AXIo8E"}},"config":{"forward":1},"text":"","sourceAd":""}"""
group = 543780931
# have error when sending group xml? why?
content="""<?xml version='1.0' encoding='UTF-8' standalone='yes' ?><msg serviceID="107" templateID="1" action="viewReceiptMessage" brief="[回执消息]" m_resid="UUAq5xccO44DIuoF23YLkxMk04EBBbGxESP6o45SqHb2KiUOmUpPUHoBkBSUwKcL" m_fileName="6862690782327914927" sourceMsgId="0" url="" flag="3" adverSign="0" multiMsgFlag="0"><item layout="29" advertiser_id="0" aid="0"><type>1</type></item><source name="" icon="" action="" appid="-1" /></msg>"""
result = action.sendGroupXml(group=group, content=content)
# result = action.sendGroupJson(group=group, content=content)
print(result)