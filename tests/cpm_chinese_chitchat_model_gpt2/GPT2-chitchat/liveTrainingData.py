def getQQGroupChatData():
    import pandas as pd
    # load sample data
    dataPaths = ["/root/Desktop/works/pyjom/tasks/qq/qq_red_packet_collect/logs/redPacketLog_0.log","/root/Desktop/works/pyjom/tasks/qq/qq_red_packet_collect/logs/redPacketLog_1.log"]
    # choose not to clean everything after the training, yet.
    # import requests
    tag = '[GROUP_TEXT_MESSAGE] '
    for dataPath in dataPaths:
        dataArray = []
        import json
        import parse
        with open(dataPath, 'r') as f:
            data = f.read()
            for line in data.split('\n'):
                line = line.strip()
                if line.startswith(tag):
                    try:
                        mJson = parse.parse(tag+"{JSON}", line)
                        mJson = json.loads(mJson['JSON'])
                        dataArray.append(mJson)
                    except:
                        pass
        df = pd.DataFrame(dataArray)
        for group_id in df['group_id'].unique():
            mData = df[group_id == df['group_id']]
        breakpoint()

if __name__ == '__main__':
    getQQGroupChatData()