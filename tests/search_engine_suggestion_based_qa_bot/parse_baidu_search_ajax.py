import pyjq

command = "(.data.cardData[] | select(.extData) | .extData.showInfo | select(. != null) | {titles, snippets,imgs_src,simi})"

from lazero.filesystem.io import readJsonObjectFromFile

obj = readJsonObjectFromFile('ajax_baidu.json')
processed_obj = pyjq.first(command,obj)
import pandas as pd
from pprint import pprint
pprint(processed_obj)
df_title_snippets = pyjq.first("{}",procecssed_obj)
# [('titles', 15), ('snippets', 15), ('imgs_src', 43), ('simi', 43)]
# 15, 15, 43, 43
# df = pd.DataFrame(processed_obj)
# print(df)
breakpoint()
