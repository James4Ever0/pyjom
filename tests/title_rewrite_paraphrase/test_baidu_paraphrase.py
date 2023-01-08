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


BAIDU_API_SLEEP_TIME = 1
BAIDU_TRANSLATOR_LOCK_FILE = (
    "/root/Desktop/works/pyjom/tests/karaoke_effects/baidu_translator.lock"
)


def baidu_lang_detect(
    content: str, sleep=BAIDU_API_SLEEP_TIME, lock_file=BAIDU_TRANSLATOR_LOCK_FILE
):  # target language must be chinese.
    import filelock

    lock = filelock.FileLock(lock_file)
    with lock:
        import time

        time.sleep(sleep)
        language_recognition_model = getBaiduLanguageRecognitionModel()
        langid = language_recognition_model.recognize(content)
        return langid


def baidu_translate(
    content: str,
    source: str,
    target: str,
    sleep: int = BAIDU_API_SLEEP_TIME,
    lock_file: str = BAIDU_TRANSLATOR_LOCK_FILE,
):  # target language must be chinese.
    import filelock

    lock = filelock.FileLock(lock_file)
    with lock:
        import time

        time.sleep(sleep)
        language_translation_model = getBaiduLanguageTranslationModel()
        translated_content = language_translation_model.translate(
            content, source, target
        )
        return translated_content


from typing import Iterable, Union

import random


def baiduParaphraserByTranslation(
    content: str,
    debug: bool = False,
    paraphrase_depth: Union[
        int, Iterable
    ] = 1,  # only 1 intermediate language, default.
    suggested_middle_languages: list[str] = [
        "zh",
        "en",
        "jp",
    ],  # english, japanese, chinese
):
    if issubclass(type(paraphrase_depth), Iterable):
        paraphrase_depth = random.choice(paraphrase_depth)

    target_language_id = baidu_lang_detect(content)

    all_middle_languages = list(set(suggested_middle_languages + [target_language_id]))

    assert paraphrase_depth > 0
    if paraphrase_depth > 1:
        assert len(all_middle_languages) >= 3

    current_language_id = target_language_id
    middle_content = content
    head_tail_indexs = set([0, paraphrase_depth - 1])

    intermediate_languages = []

    for loop_id in range(paraphrase_depth):
        forbid_langs = set([current_language_id])
        if loop_id in head_tail_indexs:
            forbid_langs.add(target_language_id)
        non_target_middle_languages = [
            langid for langid in all_middle_languages if langid not in forbid_langs
        ]
        if debug:
            print(f"INDEX: {loop_id} INTERMEDIATE LANGS: {non_target_middle_languages}")
        middle_language_id = random.choice(non_target_middle_languages)
        middle_content = baidu_translate(
            middle_content, source=current_language_id, target=middle_language_id
        )
        current_language_id = middle_language_id
        intermediate_languages.append(middle_language_id)

    output_content = baidu_translate(
        middle_content, source=current_language_id, target=target_language_id
    )
    success = output_content.strip() != content.strip()
    if debug:
        print("SOURCE LANGUAGE:", target_language_id)
        print("USING INTERMEDIATE LANGUAGES:", intermediate_languages)
        print("PARAPHRASED:", output_content)
        print("paraphrase success?", success)

    return output_content, success


# content = "世上所有小猫都是天使变的！"
content =  "支持几十个不同类型的任务，具有较好的零样本学习能力和少样本学习能力。"
output, success = baiduParaphraserByTranslation(content, paraphrase_depth=3, debug=True)
