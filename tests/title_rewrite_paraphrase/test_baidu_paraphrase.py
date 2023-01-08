
def baidu_lang_detect(content:str):
    langid = ...
    return langid

def baidu_translate(content:str,source:str, target:str):
    translated_content = ...
    return translated_content

content = "世上所有小猫都是天使变的！"

target_language_id = baidu_lang_detect(content)

all_middle_languages = [] # english, japanese, chinese

non_target_middle_languages = [langid for langid in all_middle_languages if langid is not target_language_id]

import random

middle_language_id = random.choice(non_target_middle_languages)

middle_content = baidu_translate(content, source = target_language_id, target = middle_language_id)

output_content = baidu_translate(middle_content, source = middle_language_id, target = target_language_id)

print("PARAPHRASED:", output_content)