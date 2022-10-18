from botoy import Action

qq = 917521610
port = 8784
action = Action(qq=qq, port=port, host='127.0.0.1')
user=1281727431
cover = "http://inews.gtimg.com/newsapp_bt/0/15352117085/640"
content = """<?xml version='1.0' encoding='UTF-8' standalone='yes'?><msg templateID="123" url="https://b23.tv/5K7qh7K?share_medium=android&amp;share_source=qq&amp;bbid=XY46C7C4C74C8D645671EF7E8F4CC7810054A&amp;ts=1657521142233" serviceID="1" action="web" actionData="" a_actionData="" i_actionData="" brief="[QQ小程序]哔哩哔哩" flag="0"><item layout="2"><picture cover="{}"/><title>哔哩哔哩</title><summary>【C语言】《带你学C带你飞》</summary></item><source url="https://b23.tv/5K7qh7K?share_medium=android&amp;share_source=qq&amp;bbid=XY46C7C4C74C8D645671EF7E8F4CC7810054A&amp;ts=1657521142233" icon="https://open.gtimg.cn/open/app_icon/00/95/17/76/100951776_100_m.png?t=1657091104" name="哔哩哔哩" appid="0" action="web" actionData="" a_actionData="tencent0://" i_actionData=""/></msg>""".format(cover)
result= action.sendFriendXml(user=user, content=content)
print(result)