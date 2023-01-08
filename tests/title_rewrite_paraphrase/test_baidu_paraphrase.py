
content = ""

target_language_id = ...

all_middle_languages = [] # english, japanese, chinese

non_target_middle_languages = [langid for langid in all_middle_languages if langid is not target_language_id]

import random

middle_language_id = random.choice(non_target_middle_languages)

middle_content = baidu_translate(content, source = target_language_id, target = middle_language_id)

output_content = baidu_translate(middle_content, source = middle_language_id, target = target_language_id)