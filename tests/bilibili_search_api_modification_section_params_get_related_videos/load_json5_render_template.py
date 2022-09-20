import json5

data = open("channelConfig.json5",'r').read()
data = json5.loads(data)

channelList = data['channelList']
for channel in channelList:
    channelName = channel['name']
    channelTid = channel['tid']
    for subChannel in channel['sub']:
        subChannelName = subChannel['name']
        subChanneiTid = subChannel['tid']