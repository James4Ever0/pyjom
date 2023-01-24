subtitle_types = ["ass", "srt"]
video_types = [
    "mkv",
    "mov",
    "mp4",
    "flv",
    "avi",
    "ogv",
    "webm",
    "ts",
    "wmv",
    "webm",
    "m4v",
    "3gp",
]
# use ffmpeg for subtitle extraction?
filetypes = {"subtitle": subtitle_types, "video": video_types}

Bangumi_Name = "Yahari Ore no Seishun Lovecome wa Machigatte Iru.".strip()
episodeIndex = 3

chinese_simplified_sub_types = ["chs", "简体", "简日"]
chinese_traditional_sub_types = ["繁日", "繁体", "繁體", "cht"]
import json

# replace non-alphanumeric charcters.
episode_formatter = lambda episode_index: str(episode_index).zfill(2)

import re

# also replace all double spaces.
def double_space_replacer(chars: str):
    if "  " in chars:
        chars = chars.replace("  ", " ")
        return double_space_replacer(chars)
    else:
        return chars


alphanumeric_filter = lambda chars: double_space_replacer(
    re.sub(r"[^a-z0-9]", " ", chars)
)

bangume_name_lower_alphanumeric = alphanumeric_filter(Bangumi_Name.lower())

with open("test_filenames.json", "r") as f:
    fnames = json.loads(f.read())
for fname in fnames:
    fname_lower = fname.lower()
    fname_lower_alphanumeric = alphanumeric_filter(fname_lower)
    file_extension = fname_lower.split(".")[-1]
    current_file_type = "unknown"

    for filetype, file_extensions in filetypes.items():
        if file_extension in file_extensions:
            current_file_type = filetype
            break
    print(f"<{current_file_type}> {fname}")
    print(fname_lower_alphanumeric)
    substring_location_start = fname_lower_alphanumeric.find(
        bangume_name_lower_alphanumeric
    )
    if substring_location_start!=-1:
        substring_location_end = substring_location_start + len(
        bangume_name_lower_alphanumeric
    )
        assert fname_lower_alphanumeric[substring_location_start: substring_location_end] == bangume_name_lower_alphanumeric
        episodeIndexLocation = fname_lower_alphanumeric.find(f" {episode_formatter(episodeIndex)} ")

        if episodeIndexLocation!=-1:
            if episodeIndexLocation+1>=substring_location_end:
                print("EPISODE?") # this is the index we want
                print(episodeIndex)