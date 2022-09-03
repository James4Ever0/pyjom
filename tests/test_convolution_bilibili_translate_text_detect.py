import json

# easy gig, you said.
targetFile = "/root/Desktop/works/pyjom/tests/bilibili_practices/bilibili_video_translate/japan_day.json"

mJson = json.loads(open(targetFile, 'r',encoding='utf-8').read())

mKeys = [mJson.keys()]
mIntKeys = [int(x) for x in mKeys]
