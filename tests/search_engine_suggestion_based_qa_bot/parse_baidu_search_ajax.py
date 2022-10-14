import pyjq

command = "(.data.cardData[] | select(.extData) | .extData.showInfo | select(. != null) | {titles, snippets,imgs_src,simi})"

from lazero.filesystem.io import readJsonObjectFromFile

obj = readJsonObjectFromFile("ajax_baidu.json")
processed_obj = pyjq.first(command, obj)
import pandas as pd

# from pprint import pprint
# pprint(processed_obj)
title_snippets = pyjq.first("{titles, snippets}", processed_obj)
img_sim = pyjq.first("(.simi[]|=tonumber )|{imgs_src, simi}", processed_obj)
img_sim["simi"] = img_sim["simi"]
# [('titles', 15), ('snippets', 15), ('imgs_src', 43), ('simi', 43)]
# 15, 15, 43, 43
df_title_snippets = pd.DataFrame(title_snippets)
df_img_sim = pd.DataFrame(img_sim)
print(df_title_snippets.head())
print(df_img_sim.head())
elem = df_img_sim["simi"][0]
print(type(elem), elem)  # str?
# breakpoint()
from urllib.parse import parse_qs
pre_qs = df_img_sim['imgs_src'].split("?")
# qs = parse_qs(pre_qs)
# print(qs)
print(pre_qs)