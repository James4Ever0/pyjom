curl -L -o some_lyrics.json http://localhost:4000/lyric?id=33894312

python3 extract_lyrics_from_netease_json.py some_lyrics.json
# just want the "lrc" part.