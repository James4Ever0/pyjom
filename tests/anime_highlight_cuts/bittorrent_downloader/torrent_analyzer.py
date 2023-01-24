#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

# single file.
# torrent_path = "[桜都字幕組] 不當哥哥了！ _ Onii-chan wa Oshimai! [01][1080p][繁體內嵌].torrent"

torrent_path = "[Kamigami&VCB-Studio] Yahari Ore no Seishun Lovecome wa Machigatte Iru. [Ma10p_1080p].torrent"
basepath = "/Users/jamesbrown/Downloads/anime_download"

torrent_path = os.path.join(basepath, torrent_path)

# analyze this torrent file.
import torrent_parser as tp

data = tp.parse_torrent_file(torrent_path)

import rich
rich.print(data)
# will be complete name later?
single_file = not('files' in data['info'].keys())
# data['info']['name'] 

# length will be total length?
# data['info']['length']
# breakpoint()

# does it preserve the order?
# import humanize
# well.

fnames=[]
import json
from humanfriendly import format_size
if not single_file:
    for index, fileInfo in enumerate(data['info']['files']):
        aria2c_index = index+1
        length = fileInfo['length']
        path = fileInfo['path'] # multiple strings in a list
        joined_path = "/".join(path)
        filesize_human_readable = format_size(length)
        print(f"[{aria2c_index}] ** [{filesize_human_readable}] ** {path[-1]}")
        # the index is right.
        fnames.append(path[-1])
        print(f"FULLPATH: {joined_path}")

with open("test_filenames.json",'w+') as f:
    f.write(json.dumps(fnames))