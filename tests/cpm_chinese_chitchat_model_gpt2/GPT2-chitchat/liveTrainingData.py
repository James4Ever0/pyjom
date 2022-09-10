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
            content = mData['content'].unique() # filter out shits.
            content = content.tolist()
            if len(content) >=2:
                for source, target in zip(content[:-1], content[1:]):
                    yield source, target
            else:
                print("GROUP %d DOES NOT HAVE SUFFICIENT CHATS" % group_id)
        # breakpoint()


import string
import zhon.hanzi

englishPuncturals = string.punctuation
chinesePuncturals = zhon.hanzi.punctuation

def removeChinesePunctuation(text):
    for elem in chinesePuncturals:
        text = text.replace(elem, "")
    return text

def removeLeadingAndTrailingPunctuation(text):
    for elem in englishPuncturals+chinesePuncturals:
        if text.startswith(elem):
            text = text[1:]
        if text.endswith(elem):
            if elem == ".": continue
            text = text[:-1]
    return text

def removeUnnecessaryPunctuation(text):
    text = removeChinesePunctuation(text)
    text = removeLeadingAndTrailingPunctuation(text)
    return text

if __name__ == '__main__':
    for source, target in getQQGroupChatData():
        source = removeUnnecessaryPunctuation(source)
        target = removeUnnecessaryPunctuation(target)
        if len(source) > 3 and len(target)>3:
            print("SOURCE: %s" % source)
            print("TARGET: %s" % target)
            print("_________________")