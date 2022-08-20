import pylrc

lrc_file = open('example.lrc')
lrc_string = ''.join(lrc_file.readlines())
lrc_file.close()

subs = pylrc.parse(lrc_string)
for sub in subs: