import pylrc
from MediaInfo import MediaInfo


def getMusicDuration(musicPath):
    info = MediaInfo(filename=musicPath)
    info = info.getInfo()
    # print(info)
    # breakpoint()
    length = info["duration"]
    length = float(length)
    return length


musicPath = "/root/Desktop/works/pyjom/tests/music_analysis/exciting_bgm.mp3"
musicDuration = getMusicDuration(musicPath)

lrc_file = open("/root/Desktop/works/pyjom/tests/music_analysis/exciting_bgm.lrc")
lrc_string = "".join(lrc_file.readlines())
lrc_file.close()

subs = pylrc.parse(lrc_string)

lyricDurationThresholds = (0.5, 4)

textArray = []
for sub in subs:
    startTime = sub.time
    text = sub.text
    textArray.append((startTime, text))

textArray.sort(key=lambda x: x[0])

lastStartTime = textArray[0][0]

newTextArray = [{"start": textArray[0][0], "text": textArray[0][1]}]

for startTime, text in textArray[1:]:
    if startTime - lastStartTime < lyricDurationThresholds[0]:
        continue
    else:
        lastStartTime = startTime
        newTextArray.append({"text": text, "start": startTime})

# now calculate the end time, please?
# you may want to translate this if you have to.
# when it does not contains anything in chinese.

# using deepl?
# put that aside please? focus on this shit...
import numpy as np

lyricDurations = [np.mean(lyricDurationThresholds)]

for index, elem in enumerate(newTextArray):
    text = elem["text"]
    start = elem["start"]
    nextIndex = index + 1
    if nextIndex < len(newTextArray):
        nextElem = newTextArray[nextIndex]
        nextStart = nextElem["start"]
        end = nextStart - start
        if end > lyricDurationThresholds[0] and end < lyricDurationThresholds[1]:
            lyricDurations.append(end)
        end = min(end, lyricDurationThresholds[1], musicDuration - start) + start
    else:
        end = np.mean(lyricDurations) + start
        end = min(musicDuration, end)
    newTextArray[index].update({"end": end})

for elem in newTextArray:
    print(elem)
# great. now let's do the freaking work?
