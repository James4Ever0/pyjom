def getQQGroupChatData(dataPaths = ["/root/Desktop/works/pyjom/tasks/qq/qq_red_packet_collect/logs/redPacketLog_0.log","/root/Desktop/works/pyjom/tasks/qq/qq_red_packet_collect/logs/redPacketLog_1.log"]):
    import pandas as pd
    # load sample data
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
            # not right. we need to cut it in multiple sequences.
            # import random
            if len(content) >=2:
                for source, target in zip(content[:-1], content[1:]):
                    yield source, target
            else:
                print("GROUP %d DOES NOT HAVE SUFFICIENT CHATS" % group_id)
        # breakpoint()

def clearQQGroupChatData(dataPaths = ["/root/Desktop/works/pyjom/tasks/qq/qq_red_packet_collect/logs/redPacketLog_0.log","/root/Desktop/works/pyjom/tasks/qq/qq_red_packet_collect/logs/redPacketLog_1.log"]):
    import os
    for dataPath in dataPaths:
        cmd = 'cat /dev/null > {}'.format(dataPath)
        print("CLEARING: {}".format(dataPath))
        os.system(cmd)

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

def removeUnwantedSpace(text):
    while True:
        if "  " in text:
            text = text.replace("  ", " ")
        else:
            break
    return text

if __name__ == '__main__':
    for source, target in getQQGroupChatData(): # to make it more humane?
        # source = removeUnnecessaryPunctuation(source)
        # source = removeUnwantedSpace(source)
        # target = removeUnnecessaryPunctuation(target)
        # target = removeUnwantedSpace(target)
        if len(source) > 3 and len(target)>3:
            print("SOURCE: %s" % source)
            print("TARGET: %s" % target)
            print("_________________")