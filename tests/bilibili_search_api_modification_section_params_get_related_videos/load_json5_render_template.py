import json5
import jinja2

template = open('template.j2','r').read()
template = jinja2.Template(template)

data = open("channelConfig.json5",'r').read()
data = json5.loads(data)

channelList = data['channelList']
for channel in channelList:
    try:
        channelName = channel['name']
        channelTid = channel['tid']
        subChannels = []
        for subChannel in channel['sub']:
            try:
                subChannelName = subChannel['name']
                subChannelTid = subChannel['tid']
                subChannels.append((subChannelName, subChannelTid))
            except:
                continue
        rendered_data = template.render(channelName=channelName, channelTid=channelTid, subChannels=subChannels)
        print(rendered_data)
    except:
        continue