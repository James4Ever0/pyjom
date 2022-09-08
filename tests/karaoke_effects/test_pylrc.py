import pylrc

lrc_file = open('/root/Desktop/works/pyjom/tests/music_analysis/exciting_bgm.lrc')
lrc_string = ''.join(lrc_file.readlines())
lrc_file.close()

subs = pylrc.parse(lrc_string)

lyricDurationThreshold = 4

for sub in subs:
    print(sub.time) # single shit.
    # print(dir(sub))
    text = sub.text
    print(text)