import json5

data = open("channelConfig.json5",'r').read()
data = json5.loads(data)

channelList = data['channelList']
for channel in channelList:
    channelName = channel['name']
    channel_tid = channel['tid']
    for subchannel in channel['sub']:
        