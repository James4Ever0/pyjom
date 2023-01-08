
from functools import lru_cache
import paddlehub as hub

@lru_cache(maxsize=1)
def getBaiduLanguageTranslationModel():
    language_translation_model = hub.Module(name="baidu_translate")
    return language_translation_model


@lru_cache(maxsize=1)
def getBaiduLanguageRecognitionModel():
    language_recognition_model = hub.Module(name="baidu_language_recognition")
    return language_recognition_model

# text = "hello world"
# "zh", 'en', 'jp'
# text = "請輸入要轉換簡繁體的中文漢字" # zh
text = "私は日本人です"
language_code = language_recognition_model.recognize(text)
print("language_code: %s" % language_code)

BAIDU_API_SLEEP_TIME=1
BAIDU_TRANSLATOR_LOCK_FILE="/root/Desktop/works/pyjom/tests/karaoke_effects/baidu_translator.lock"
def baidu_lang_detect(content:str, sleep=BAIDU_API_SLEEP_TIME,lock_file=BAIDU_TRANSLATOR_LOCK_FILE):  # target language must be chinese.
    import filelock

    lock = filelock.FileLock(
        lock_file
    )
    with lock:
        import time

        time.sleep(sleep)
        langid = ...
        return langid

def baidu_translate(content:str,source:str, target:str,sleep:int= BAIDU_API_SLEEP_TIME,lock_file:str=BAIDU_TRANSLATOR_LOCK_FILE):  # target language must be chinese.
    import filelock

    lock = filelock.FileLock(
        lock_file
    )
    with lock:
        import time

        time.sleep(sleep)
        translated_content = ...
        return translated_content

content = "世上所有小猫都是天使变的！"

target_language_id = baidu_lang_detect(content)

all_middle_languages = ["zh", 'en', 'jp'] # english, japanese, chinese

non_target_middle_languages = [langid for langid in all_middle_languages if langid is not target_language_id]

import random

middle_language_id = random.choice(non_target_middle_languages)

middle_content = baidu_translate(content, source = target_language_id, target = middle_language_id)

output_content = baidu_translate(middle_content, source = middle_language_id, target = target_language_id)

print("PARAPHRASED:", output_content)