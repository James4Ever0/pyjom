subtitle_types = ["ass",'srt']
video_types = ['mkv','mov','mp4','flv','avi','ogv','webm','ts','wmv','webm','m4v','3gp']
# use ffmpeg for subtitle extraction?
import json
with open("test_filenames.json",'w+') as f:
    fnames = json.loads(f.read())
for fname in fnames:
    