import json
import sys

json_file = sys.argv[1]
assert json_file.endswith(".json")

with open(json_file,"r", encoding="utf-8") as f:
    json_data = json.loads(f.read())
    lrc = json_data["lrc"]
    version = lrc["version"]
    lyric = lrc["lyric"]
    with open(json_file+".lrc","w") as f0: f0.write(lyric)