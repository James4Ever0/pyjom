import pyjq

command = "(.data.cardData[] | select(.extData) | .extData.showInfo | select(. != null) | {titles, snippets,imgs_src,simi})"

from lazero.filesystem.io import readJsonObjectFromFile

obj = readJsonObjectFromFile('ajax_baidu.json')
processed_obj = pyjq.first(command,obj)
import pandas as pd
df = pd.DataFrame(processed_obj)
print(df)