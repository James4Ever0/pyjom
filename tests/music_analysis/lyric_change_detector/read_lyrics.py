import pylrc

with open("some_lyrics.json.lrc","r") as f:
    lrc_string = f.read()
    subs = pylrc.parse(lrc_string)
    for sub in subs:
        time_in_secs = sub.time
        content = sub.text
    # skip those which are too short.
    # print(subs)
    # breakpoint()