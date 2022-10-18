baseUrl = "http://0.0.0.0:5700"

# try to send xml to group.
# 私聊可以发xml 但是群聊不行 群聊只能发加密好验证好的json
# cover = "http://pubminishare-30161.picsz.qpic.cn/d4ad36fa-833e-4018-b994-a2da810f2d54"
# content = """<?xml version='1.0' encoding='UTF-8' standalone='yes'?><msg templateID="123" url="https://b23.tv/5K7qh7K?share_medium=android&amp;share_source=qq&amp;bbid=XY46C7C4C74C8D645671EF7E8F4CC7810054A&amp;ts=1657521142233" serviceID="1" action="web" actionData="" a_actionData="" i_actionData="" brief="[QQ小程序]哔哩哔哩" flag="0"><item layout="2"><picture cover="{}"/><title>哔哩哔哩</title><summary>【C语言】《带你学C带你飞》</summary></item><source url="https://b23.tv/5K7qh7K?share_medium=android&amp;share_source=qq&amp;bbid=XY46C7C4C74C8D645671EF7E8F4CC7810054A&amp;ts=1657521142233" icon="https://open.gtimg.cn/open/app_icon/00/95/17/76/100951776_100_m.png?t=1657091104" name="哔哩哔哩" appid="0" action="web" actionData="" a_actionData="tencent0://" i_actionData=""/></msg>""".format(
# cover)
group = 543780931

import requests

url = baseUrl + "/send_group_msg"
# message = 'test'
# content = """<?xml version="1.0" encoding="UTF-8" standalone="yes" ?><msg serviceID="2" templateID="1" action="web" brief="" sourceMsgId="0" url="https://qm.qq.com/cgi-bin/qm/qr?k=wyw10nH14NxBzBmM2DZK_bj9y9yX-IJL" flag="0" adverSign="0" multiMsgFlag="0"><item layout="2"><audio cover="https://python3student.github.io/img/avatar.jpg" src="https://music.163.com/song/media/outer/url?id=449818326.mp3" /><title>鹿 be free</title><summary>『作者』神奇</summary></item><source name="神奇永远的神！" icon="https://python3student.github.io/img/avatar.jpg" url="https://python3student.github.io/img/avatar.jpg" action="app" a_actionData="com.netease.cloudmusic" i_actionData="tencent100495085://" appid="100495085" /></msg>"""
# content = """<?xml version='1.0' encoding='UTF-8' standalone='yes' ?><msg serviceID="2" templateID="1" action="web" brief="&#91;分享&#93; 十年" sourceMsgId="0" url="https://i.y.qq.com/v8/playsong.html?_wv=1&amp;songid=4830342&amp;souce=qqshare&amp;source=qqshare&amp;ADTAG=qqshare" flag="0" adverSign="0" multiMsgFlag="0" ><item layout="2"><audio cover="http://imgcache.qq.com/music/photo/album_500/26/500_albumpic_89526_0.jpg" src="http://ws.stream.qqmusic.qq.com/C400003mAan70zUy5O.m4a?guid=1535153710&amp;vkey=D5315B8C0603653592AD4879A8A3742177F59D582A7A86546E24DD7F282C3ACF81526C76E293E57EA1E42CF19881C561275D919233333ADE&amp;uin=&amp;fromtag=3" /><title>十年</title><summary>陈奕迅</summary></item><source name="QQ音乐" icon="https://i.gtimg.cn/open/app_icon/01/07/98/56/1101079856_100_m.png" url="http://web.p.qq.com/qqmpmobile/aio/app.html?id=1101079856" action="app"  a_actionData="com.tencent.qqmusic" i_actionData="tencent1101079856://" appid="1101079856" /></msg>"""
# content = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?><msg serviceID="1" templateID="1" action="" brief="QQ红包" sourceMsgId="0" flag="8" adverSign="0" multiMsgFlag="0"><item layout="6"><title color="#EE00EE" style="4">阿深真帅</title><summary color="#9A32CD">是不是很无语</summary><picture cover="http://t1.hddhhn.com/uploads/tu/20150507/20405-eBE9jO.jpg" action="web" url="http://url.cn/5g4eOiY" w="0" h="0"/></item></msg>"""
# message = "[CQ:xml,data={}]".format(content) # xml thing.
# content="""{"app":"com.tencent.miniapp_01"&#44;"desc":"哔哩哔哩"&#44;"view":"view_8C8E89B49BE609866298ADDFF2DBABA4"&#44;"ver":"1.0.0.19"&#44;"prompt":"&#91;QQ小程序&#93;哔哩哔哩"&#44;"meta":{"detail_1":{"appType":0&#44;"appid":"1109937557"&#44;"desc":"Appium 手机 App 自动化 + Python"&#44;"gamePoints":""&#44;"gamePointsUrl":""&#44;"host":{"nick":"Yukio"&#44;"uin":1281727431}&#44;"icon":"https:\/\/open.gtimg.cn\/open\/app_icon\/00\/95\/17\/76\/100951776_100_m.png?t=1659061321"&#44;"preview":"pubminishare-30161.picsz.qpic.cn\/a0b8d306-5b6d-4b27-9539-021a2adcc264"&#44;"qqdocurl":"https:\/\/b23.tv\/4hWdtET?share_medium=android&amp;share_source=qq&amp;bbid=XY1BB721B1F97348DBDE4297FE1B4ABE26BAA&amp;ts=1665924308147"&#44;"scene":1036&#44;"shareTemplateData":{}&#44;"shareTemplateId":"8C8E89B49BE609866298ADDFF2DBABA4"&#44;"showLittleTail":""&#44;"title":"哔哩哔哩"&#44;"url":"m.q.qq.com\/a\/s\/ea6d34b58a6a6209cd5088c436a254de"}}&#44;"config":{"autoSize":0&#44;"ctime":1665924338&#44;"forward":1&#44;"height":0&#44;"token":"a2458ec4231b7b8204c717f3a955a9fc"&#44;"type":"normal"&#44;"width":0}}"""
content = """{"app":"com.tencent.structmsg"&#44;"desc":"新闻"&#44;"view":"news"&#44;"ver":"0.0.0.1"&#44;"prompt":"&#91;分享&#93;哔哩哔哩"&#44;"meta":{"news":{"action":""&#44;"android_pkg_name":""&#44;"app_type":1&#44;"appid":100951776&#44;"ctime":1666081902&#44;"desc":"外国博主英文讲解：二十大为什么如此重要？"&#44;"jumpUrl":"https:\/\/b23.tv\/B64KMQq?share_medium=android&amp;share_source=qq&amp;bbid=XY1BB721B1F97348DBDE4297FE1B4ABE26BAA&amp;ts=1666081860133"&#44;"preview":"https:\/\/pic.ugcimg.cn\/58a74c8432a80e7e2de612e6e53e37f3\/jpg1"&#44;"source_icon":"https:\/\/open.gtimg.cn\/open\/app_icon\/00\/95\/17\/76\/100951776_100_m.png?t=1659061321"&#44;"source_url":""&#44;"tag":"哔哩哔哩"&#44;"title":"哔哩哔哩"&#44;"uin":1281727431}}&#44;"config":{"ctime":1666081902&#44;"forward":true&#44;"token":"d7cc3a93e7c3a9acd1c8662157e3e5fb"&#44;"type":"normal"}}"""
# content = """{"app":"com.tencent.structmsg"&#44;"desc":"音乐"&#44;"view":"music"&#44;"ver":"0.0.0.1"&#44;"prompt":""&#44;"meta":{}}"""
# content = (
    # """{"app":"com.tencent.structmsg","desc":"","view":"singleImg","ver":"0.0.0.1","prompt":"邪少QQXML论坛","appID":"","sourceName":"","actionData":"","actionData_A":"","sourceUrl":"","meta":{"singleImg":{"mainImage":"https://gchat.qpic.cn/gchatpic_new/3020005669/916530575-2949639428-6E45D21EADE33511C565E25AB432AB59/0?term=2","mainUrl":""}},"text":"","extraApps":[],"sourceAd":"","config":{"forward":1}}""".replace(
#         "&", "&amp;"
#     )
#     .replace(",", "&#44;")
#     .replace("[", "&#91;")
#     .replace("]", "&#93;")
# )


# the token is likely to be some checksum, md5 or something. some aes/rsa?
message = "[CQ:json,data={}]".format(content)  # json thing.
# message = "[CQ:tts,text=嘤嘤嘤]"
# content = """<?xml version='1.0' encoding='UTF-8' standalone='yes' ?><msg serviceID="2" templateID="1" action="web" brief="&#91;分享&#93; 十年" sourceMsgId="0" url="http://music.163.com/m/song/409650368" flag="0" adverSign="0" multiMsgFlag="0" ><item layout="2"><audio cover="http://p2.music.126.net/g-Qgb9ibk9Wp_0HWra0xQQ==/16636710440565853.jpg?param=90y90" src="https://music.163.com/song/media/outer/url?id=409650368.mp3" /><title>十年</title><summary>黄梦之</summary></item><source name="网易云音乐" icon="https://pic.rmb.bdstatic.com/911423bee2bef937975b29b265d737b3.png" url="http://web.p.qq.com/qqmpmobile/aio/app.html?id=1101079856" action="app" a_actionData="com.netease.cloudmusic" i_actionData="tencent100495085://" appid="100495085" /></msg>"""
# message = '[CQ:xml,data={}]'.format(content)
data = {"group_id": group, "message": message, "auto_escape": False}
r = requests.post(url, data=data)
print(r.json())
# cannot send json. wtf?
# 请参考 go-cqhttp 端输出
