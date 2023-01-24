subtitle_types = ["ass",'srt']
video_types = ['mkv','mov','mp4','flv','avi','ogv','webm','ts','wmv','webm','m4v','3gp']
# use ffmpeg for subtitle extraction?
filetypes = {'subtitle':subtitle_types,'video':video_types}

Bangumi_Name = 'Yahari Ore no Seishun Lovecome wa Machigatte Iru.'

import json

episode_formatter = lambda eposide_index: ["{}","[{}]",""]

with open("test_filenames.json",'r') as f:
    fnames = json.loads(f.read())
for fname in fnames:
    fname_lower = fname.lower()
    file_extension = fname_lower.split(".")[-1]
    current_file_type= "unknown"

    for filetype, file_extensions in filetypes.items():
        if file_extension in file_extensions:
            current_file_type = filetype
            break
    print(f"<{current_file_type}> {fname}")