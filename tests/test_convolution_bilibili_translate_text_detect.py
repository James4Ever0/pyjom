import json

# easy gig, you said.
targetFile = "/root/Desktop/works/pyjom/tests/bilibili_practices/bilibili_video_translate/japan_day.json"

mJson = json.loads(open(targetFile, 'r',encoding='utf-8').read())

mKeys = list(mJson.keys())
mIntKeys = [int(x) for x in mKeys]
minKey, maxKey = min(mIntKeys), max(mIntKeys)

for intKey in range(minKey, maxKey+1):
    strKey = str(intKey)
    target = mJson[strKey]
    for item in target:
        location = item[0]
        text, confidence = item[1]
        print(location)
    # print(intKey,target)
    # this time we do not care about the text inside.
    # breakpoint()