# simply copy train shit as test shit.

from commons import load_train_data_core, import_word

Word = import_word()
import json
data = []
import os

data_dir = "/media/root/help/pyjom/tests/title_cover_generator/GPT2-NewsTitle/data_dir"
if not os.path.exists(data_dir):
    os.mkdir(data_dir)

train_file = os.path.join(data_dir,"train_data.json")
test_file = os.path.join(data_dir,"test_data.json")

for content, title in load_train_data_core():
    sample = {"title": title[0],"content":content[0]}
    data.append(sample) # is that necessary?

with open(train_file,"w+",encoding="utf8") as f:
    f.write(json.dumps(data,ensure_ascii=False,indent=4))

import shutil

shutil.copy(train_file, test_file)