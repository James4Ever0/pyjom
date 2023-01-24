subtitle_types = ["ass",'srt']
video_types = ['mkv','mov','mp4','flv','avi','ogv','webm','ts','wmv','webm','m4v','3gp']
# use ffmpeg for subtitle extraction?
filetypes = {'subtitle':subtitle_types,'video':video_types}

import json
with open("test_filenames.json",'w+') as f:
    fnames = json.loads(f.read())
for fname in fnames:
    fname_lower = fname.lower()
    file_extension = fname_lower.split(".")[-1]
    file_type= "unknown"

    for filetype, file_extensions in filetypes.items():
        if file_extension in file_extensions:
            print("file type:")