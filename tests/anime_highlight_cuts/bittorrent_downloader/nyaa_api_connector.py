#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests

url = "https://nyaa.si" # change this to mirror sites.

MIN_SEEDERS=7 # must be greater than this.

query = "oniichan wa oshimai! 01"
sort_term = "seeders"


anime_categories = {
    "Anime": "1_0",
    "Anime - Anime Music Video": "1_1",
    "Anime - English-translated": "1_2",
    "Anime - Non-English-translated": "1_3",
    "Anime - Raw": "1_4",
}

category_code = anime_categories["Anime"]  # anime
page = 1  # start page: 1
end_of_page = False

# better not to use rss version since it will not sort terms.

params = dict(f=0, c=category_code, q=query, s=sort_term, o="desc", p=page)

# better parse it yourself first huh?

# r = requests.get(url, params=params)
# assert r.code == 200
# text = r.text

with open("output.html", "r") as f:
    text = f.read()

from bs4 import BeautifulSoup

# with open("output.html",'w+') as f:
#    f.write(text)
soup = BeautifulSoup(text, "html.parser")
# breakpoint()

import parse

template = "Displaying results {start:d}-{end:d} out of {total:d} results."

banner = soup.find("div", class_="pagination-page-info").text
pagination_info = banner.split("\n")[0]

pagination_info_result = parse.parse(template, pagination_info)

if pagination_info_result:
    if pagination_info_result["total"] == pagination_info_result["end"]:
        print("Reached end of page.")
        end_of_page = True

from NyaaPy import utils

SITE = utils.TorrentSite.NYAASI
json_info = utils.parse_nyaa(request_text=text, limit=None, site=SITE)

import rich

rich.print(json_info)

# breakpoint()
for videoInfo in json_info:
    seeders = int(videoInfo['seeders'])
    seeders_enough = seeders>=MIN_SEEDERS
    print('seeders?',seeders)
    print("seeders enough?", seeders_enough)
    # videoInfo['id'] -> "https://nyaa.si/view/{}"

# you can also download torrent file for only file info.