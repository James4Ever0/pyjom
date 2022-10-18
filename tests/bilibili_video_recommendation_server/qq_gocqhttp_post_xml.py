baseUrl = "http://0.0.0.0:5700"

# try to send xml to group.
cover = "http://pubminishare-30161.picsz.qpic.cn/d4ad36fa-833e-4018-b994-a2da810f2d54"
content = """<?xml version='1.0' encoding='UTF-8' standalone='yes'?><msg templateID="123" url="https://b23.tv/5K7qh7K?share_medium=android&amp;share_source=qq&amp;bbid=XY46C7C4C74C8D645671EF7E8F4CC7810054A&amp;ts=1657521142233" serviceID="1" action="web" actionData="" a_actionData="" i_actionData="" brief="[QQ小程序]哔哩哔哩" flag="0"><item layout="2"><picture cover="{}"/><title>哔哩哔哩</title><summary>【C语言】《带你学C带你飞》</summary></item><source url="https://b23.tv/5K7qh7K?share_medium=android&amp;share_source=qq&amp;bbid=XY46C7C4C74C8D645671EF7E8F4CC7810054A&amp;ts=1657521142233" icon="https://open.gtimg.cn/open/app_icon/00/95/17/76/100951776_100_m.png?t=1657091104" name="哔哩哔哩" appid="0" action="web" actionData="" a_actionData="tencent0://" i_actionData=""/></msg>""".format(
cover)
group = 543780931

import requests

url = baseUrl +"/send_group_msg"
message = "" # xml thing.
data = {'group_id':group, 'message':message,'auto_escape':False}
requests.get(url,data=data)