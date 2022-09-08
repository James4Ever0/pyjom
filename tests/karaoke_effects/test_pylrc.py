import pylrc

lrc_file = open('/root/Desktop/works/pyjom/tests/music_analysis/exciting_bgm.lrc')
lrc_string = ''.join(lrc_file.readlines())
lrc_file.close()

subs = pylrc.parse(lrc_string)

lyricDurationThresholds = (0.5,4)

textArray = []
for sub in subs:
    startTime = sub.time
    text = sub.text
    textArray.append((startTime, text))

textArray.sort(lambda x: x[0])

lastStartTime = textArray[0][0]

newTextArray = [textArray[0].copy()]

for startTime, text in textArray[1:]:
    if startTime-lastStartTime < lyricDurationThresholds[0]:
        continue
    else:
        