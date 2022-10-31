cover = "https://i0.hdslb.com/bfs/archive/c5a0d18ee077fb6a4ac0970ccb0a3788e137d14f.jpg" # works.
content = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?><msg templateID="123" url="https://b23.tv/uHML5mi?share_medium=android&amp;share_source=qq&amp;bbid=XY1BB721B1F97348DBDE4297FE1B4ABE26BAA&amp;ts=1666023406285" serviceID="1" action="web" actionData="" a_actionData="" i_actionData="" brief="[QQ小程序]哔哩哔哩" flag="0"><item layout="2"><picture cover="{}"/><title>【AI动画】妮露PV动画 风转换【NovelAI】</title></item><source url="https://b23.tv/uHML5mi?share_medium=android&amp;share_source=qq&amp;bbid=XY1BB721B1F97348DBDE4297FE1B4ABE26BAA&amp;ts=1666023406285" icon="http://miniapp.gtimg.cn/public/appicon/432b76be3a548fc128acaa6c1ec90131_200.jpg" name="哔哩哔哩" appid="0" action="app" actionData="" a_actionData="tencent0://" i_actionData=""/></msg>""".format(cover)


qq = 917521610
user = 1281727431

group = 543780931

baseUrl = "http://0.0.0.0:5700" # the thing is not ready yet.

import requests

url = baseUrl + "/send_private_msg"
message = '[CQ:share,url=http://baidu.com,title=百度]'

data = {"user_id": user, "message": message, "auto_escape": False}
r = requests.post(url, data=data)
print(r.json())

# message = "[CQ:forward,id={}]".format(291457889)

# url = baseUrl+"/send_group_msg"
# data = {"group_id":group, "message": message, "auto_escape": False}

# r = requests.post(url,data=data)
# print(r.json())