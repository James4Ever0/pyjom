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
    # print(sub.time) # single shit.
    # print(dir(sub))
    # print(text)