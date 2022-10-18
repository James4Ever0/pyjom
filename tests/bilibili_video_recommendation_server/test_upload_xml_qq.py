from botoy import Action

qq = 917521610
port = 8784
action = Action(qq=qq, port=port, host='127.0.0.1')
user=1281727431
# but the goddamn xml format is not right.
# cover = "http://inews.gtimg.com/newsapp_bt/0/15352117085/640"
# cover = "http://pubminishare-30161.picsz.qpic.cn/d4ad36fa-833e-4018-b994-a2da810f2d54"
cover = "https://i0.hdslb.com/bfs/archive/c5a0d18ee077fb6a4ac0970ccb0a3788e137d14f.jpg" # works.
# content = """<?xml version='1.0' encoding='UTF-8' standalone='yes'?><msg templateID="123" url="https://b23.tv/5K7qh7K?share_medium=android&amp;share_source=qq&amp;bbid=XY46C7C4C74C8D645671EF7E8F4CC7810054A&amp;ts=1657521142233" serviceID="1" action="web" actionData="" a_actionData="" i_actionData="" brief="[QQ小程序]哔哩哔哩" flag="0"><item layout="2"><picture cover="{}"/><title>哔哩哔哩</title><summary>【C语言】《带你学C带你飞》</summary></item><source url="https://b23.tv/5K7qh7K?share_medium=android&amp;share_source=qq&amp;bbid=XY46C7C4C74C8D645671EF7E8F4CC7810054A&amp;ts=1657521142233" icon="https://open.gtimg.cn/open/app_icon/00/95/17/76/100951776_100_m.png?t=1657091104" name="哔哩哔哩" appid="0" action="web" actionData="" a_actionData="tencent0://" i_actionData=""/></msg>""".format(cover)
content = """<msg templateID="123" url="https://b23.tv/uHML5mi?share_medium=android&amp;share_source=qq&amp;bbid=XY1BB721B1F97348DBDE4297FE1B4ABE26BAA&amp;ts=1666023406285" serviceID="1" action="web" actionData="" a_actionData="" i_actionData="" brief="[QQ小程序]哔哩哔哩" flag="0"><item layout="2"><picture cover="{}"/><title>【AI动画】妮露PV动画 风转换【NovelAI】</title></item><source url="https://b23.tv/uHML5mi?share_medium=android&amp;share_source=qq&amp;bbid=XY1BB721B1F97348DBDE4297FE1B4ABE26BAA&amp;ts=1666023406285" icon="http://miniapp.gtimg.cn/public/appicon/432b76be3a548fc128acaa6c1ec90131_200.jpg" name="哔哩哔哩" appid="0" action="web" actionData="" a_actionData="tencent0://" i_actionData=""/></msg>""".format(cover)
# i guess, it is just the way it send the data is different.
result= action.sendFriendXml(user=user, content=content)
print(result)