########################[FILTERING]#########################

# DONE: use notofu for rendering then use tesseract for recognition

import pygame
import functools


@functools.lru_cache(maxsize=1)
def initPygame():
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    # headless pygame
    pygame.init()


import os
import pytesseract


def renderSingleLineTextUsingFont(
    textContent: str,
    output_name: str,
    fontPath: str = os.path.join(
        os.dirname(__file__),
        "../tests/render_and_recognize_long_text_to_filter_unwanted_characters/get_and_merge_fonts/GoNotoCurrent.ttf",
    ),
    fontSize: int = 40,
    margin: int = 20,
):
    assert os.path.exists(fontPath)
    initPygame()
    black, white = pygame.Color("black"), pygame.Color("white")

    # pillow can also do that
    # https://plainenglish.io/blog/generating-text-on-image-with-python-eefe4430fe77

    # pygame.font.get_fonts()
    # install your font to system please? but why all lower case font names?

    # fontName = "notosans"
    # this font is bad.

    # font = pygame.font.SysFont(fontName,fontSize)
    # fontPath = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf" # shit this fails.
    # use some kind of super large merged notofont.

    font = pygame.font.Font(fontPath, fontSize)

    word_surface = font.render(textContent, False, black)
    word_width, word_height = word_surface.get_size()

    SIZE = (word_width + margin * 2, word_height + margin * 2)

    image = pygame.display.set_mode(SIZE, pygame.RESIZABLE)
    image.fill(white)
    image.blit(word_surface, (margin, margin))
    pygame.display.update()
    pygame.image.save(image, output_name)


def recognizeCharactersFromImageWithTesseract(
    imagePath: str, langs: list = ["eng", "chi_sim", "chi_tra", "jpn"]
):
    # pytesseract.get_languages(config="")
    langCode = "+".join(langs)
    output = pytesseract.image_to_string(imagePath, lang=langCode)
    return output


import tempfile


def convertToChineseOrEnglishOrJapaneseCharactersUsingTesseract(char_list: str):
    with tempfile.NamedTemporaryFile("wb", suffix=".png") as f:
        imagePath = f.name
        renderSingleLineTextUsingFont(char_list,imagePath)
        output = recognizeCharactersFromImageWithTesseract(imagePath)
        return output


# bilibili title requirements may also applied to tags, descriptions

import re

import string as string_builtin
from zhon.hanzi import punctuation as chinese_punctuation


def filterNonChineseOrEnglishOrJapaneseCharacters(char_list: str):
    output = []
    checkers = {
        "chinese": lambda c: (
            (c in chinese_punctuation) or (re.match(r"[\u4e00-\u9fa5]", c) is not None)
        ),
        "english": lambda c: (
            (c in " " + string_builtin.punctuation)
            or (re.match(r"[a-zA-Z0-9]", c) is not None)
        ),
        "japanese": lambda c: re.match(r"[一-龠ぁ-ゔァ-ヴーａ-ｚＡ-Ｚ０-９々〆〤ヶ]", c) is not None,
    }
    for char in char_list:
        signal = True
        for key, checker in checkers.items():
            signal = checker(char)
            if signal in [False, 0, None]:
                break
        if signal:
            output.append(char)
    return "".join(output)


########################[FILTERING]#########################

########################[PREPROCESSING & TOPIC MODELING]#########################
englishNLP = None
englishStopWords = None
porterStemmer = None


def get_topics(model, feature_names, n_top_words):
    # 首先是遍历模型中存储的话题序号和话题内容
    topics = []
    for topic_idx, topic in enumerate(model.components_):
        # 然后打印话题的序号以及指定数量的最高频的关键词
        message = "topic #%d:" % topic_idx
        mList = [feature_names[i] for i in topic.argsort()[: -n_top_words - 1 : -1]]
        mListStr = " ".join(mList)
        message += mListStr
        mSet = set(mList)  # the set contains word groups like 'river question'
        cDict = {k: mList.count(k) for k in mSet}
        mRealList = mListStr.split(" ")
        mRealList = [
            x.strip() for x in mRealList if len(x.strip()) > 1
        ]  # usually things shorter than 2 letters are no good.
        mRealSet = set(mRealList)
        cRealDict = {k: mRealList.count(k) for k in mRealSet}
        topics.append({"combined": mList, "separate": mRealList})
    return topics


def print_topics(model, feature_names, n_top_words):
    # 首先是遍历模型中存储的话题序号和话题内容
    for topic_idx, topic in enumerate(model.components_):
        # 然后打印话题的序号以及指定数量的最高频的关键词
        message = "topic #%d:" % topic_idx
        mList = [feature_names[i] for i in topic.argsort()[: -n_top_words - 1 : -1]]
        mListStr = " ".join(mList)
        message += mListStr
        mSet = set(mList)  # the set contains word groups like 'river question'
        cDict = {k: mList.count(k) for k in mSet}
        mRealList = mListStr.split(" ")
        mRealList = [
            x.strip() for x in mRealList if len(x.strip()) > 1
        ]  # usually things shorter than 2 letters are no good.
        mRealSet = set(mRealList)
        cRealDict = {k: mRealList.count(k) for k in mRealSet}

        print("MESSAGE", message)
        print("SET", mSet)
        print("COUNT DICT", cDict)  # pointless to count here?
        print("RealSET", mRealSet)
        print("RealCOUNT DICT", cRealDict)
    print()


def englishSentencePreprocessing(
    text, unwantedPOS=["PRON", "CCONJ", "ADP", "PART", "PUNCT", "AUX"]
):
    global englishNLP, englishStopWords, porterStemmer
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize
    import en_core_web_sm
    from nltk.stem import PorterStemmer

    if englishNLP is None:
        englishNLP = en_core_web_sm.load()
    doc = englishNLP(text)
    if englishStopWords is None:
        set(stopwords.words("english"))
        englishStopWords = set([elem.lower() for elem in stopwords.words("english")])
    if porterStemmer is None:
        porterStemmer = PorterStemmer()
    lemma_word1 = []
    # this shit has the lang tag. it might be useful for language detection. really?
    for token in doc:
        if token.pos_ in unwantedPOS:
            continue
        if token.text.lower() in englishStopWords:
            continue
        lemma_word1.append(token.text)

    Stem_words = []
    for w in lemma_word1:
        rootWord = porterStemmer.stem(w)
        Stem_words.append(rootWord)
    return Stem_words


def sentenceFlatten(sentence, padding=" "):
    assert len(padding) == 1
    assert type(padding) == str
    for x in "\n\r\t":
        sentence = sentence.replace(x, padding)
    while True:
        if padding * 2 in sentence:
            sentence = sentence.replace(padding * 2, padding)
        else:
            break
    sentence = sentence.strip()
    return sentence


def englishTopicModeling(sentences, n_top_words=10, ngram_range=(1, 2), n_components=5):
    try:
        dataList = []
        for sentence in sentences:
            sentence = sentenceFlatten(sentence)
            row = englishSentencePreprocessing(sentence)
            if len(row) > 0:
                elem = " ".join(row)
                dataList.append(elem)

        data = "\n".join(dataList)

        from sklearn.feature_extraction.text import TfidfVectorizer

        # 创建一个CountVectoerizer实例
        tfidf = TfidfVectorizer(ngram_range=ngram_range)
        # 打开刚刚保存的txt文档
        from io import StringIO

        f = StringIO(data)
        # 使用CountVectorizer拟合数据
        x_train = tfidf.fit_transform(f)

        from sklearn.decomposition import LatentDirichletAllocation

        lda = LatentDirichletAllocation(n_components=n_components)
        lda.fit(x_train)

        topics = get_topics(lda, tfidf.get_feature_names(), n_top_words)
    except:
        import traceback

        traceback.print_exc()
        topics = []
    return topics


from functools import lru_cache
from lazero.utils.logger import traceError

# import os
@lru_cache(maxsize=1)
def getChineseStopWords(
    stopwordFileList=[
        "/root/Desktop/works/pyjom/tests/stopwords/chinese_stopwords.txt",
        "/root/Desktop/works/pyjom/tests/stopwords/stopwords-zh/stopwords-zh.json",
    ]
):
    import json

    stopwords = []
    for filename in stopwordFileList:
        # if os.path.exists(filename) and os.path.isfile(filename):
        try:
            with open(filename, "r") as f:
                content = f.read()
            if filename.endswith(".json"):
                try:
                    mList = json.loads(content)
                    assert type(mList) == list
                    stopwords += mList
                except:
                    traceError(_breakpoint=True)
            else:
                mList = content.split("\n")
                mList = [x.replace("\n", "").strip() for x in mList]
                mList = [x for x in mList if len(x) > 0]
                stopwords += mList
        except:
            traceError(_breakpoint=True)
    return list(set(stopwords))


def chineseSentencePreprocessing(sentence):
    import jieba
    import string
    from zhon.hanzi import punctuation

    chinese_stopwords = getChineseStopWords()
    words = jieba.lcut(sentence)
    rows = []
    for word in words:
        word = word.strip()
        if word in punctuation:
            continue
        elif word in string.punctuation:
            continue
        elif word in chinese_stopwords:
            continue
        rows.append(word)
    return rows


def chineseTopicModeling(sentences, n_top_words=10, ngram_range=(1, 2), n_components=5):
    try:
        dataList = []
        for sentence in sentences:
            sentence = sentenceFlatten(sentence)
            row = chineseSentencePreprocessing(sentence)
            if len(row) > 0:
                elem = " ".join(row)
                dataList.append(elem)

        data = "\n".join(dataList)

        from sklearn.feature_extraction.text import TfidfVectorizer

        # 创建一个CountVectoerizer实例
        tfidf = TfidfVectorizer(ngram_range=ngram_range)
        # 打开刚刚保存的txt文档
        from io import StringIO

        f = StringIO(data)
        # 使用CountVectorizer拟合数据
        x_train = tfidf.fit_transform(f)

        from sklearn.decomposition import LatentDirichletAllocation

        lda = LatentDirichletAllocation(n_components=n_components)
        lda.fit(x_train)

        topics = get_topics(lda, tfidf.get_feature_names(), n_top_words)
    except:
        import traceback

        traceback.print_exc()
        topics = []
    return topics


########################[PREPROCESSING & TOPIC MODELING]#########################


from typing import Literal

########################[PARAPHRASING]########################


def chineseParaphraserAPI(
    content: str,
    debug: bool = False,
    target_id: int = 0,
    timeout: int = 10,
    providers: list[str] = [
        "http://www.wzwyc.com/api.php?key=",
        "http://ai.guiyigs.com/api.php?key=",
    ],  # it is about to close! fuck. "本站于2023年2月19日关站" buy code from "1900373358"
):
    import requests

    target = providers[target_id]  # all the same?
    data = {"info": content}

    # target = "http://www.xiaofamaoai.com/result.php"
    # xfm_uid = "342206661e655450c1c37836d23dc3eb"
    # data = {"contents":content, "xfm_uid":xfm_uid, "agreement":"on"}
    # nothing? fuck?

    r = requests.post(target, data=data, timeout=timeout)
    output = r.text
    success = output.strip() != content.strip()
    if debug:
        print(output)
    return output, success


import clueai


@lru_cache(maxsize=1)
def getClueAIClient(apiKey: str):
    if apiKey == "":
        return clueai.Client("", check_api_key=False)
    else:
        return clueai.Client(apiKey)


def clueAIParaphraser(
    title: str,
    apiKey: str = "",
    generate_config: dict = {
        "do_sample": True,
        "top_p": 0.8,
        "max_length": 128,  # notice! not too long.
        "min_length": 5,
        "length_penalty": 1.0,
        "num_beams": 1,
    },
    prompt_template: str = """
生成与下列文字相同意思的句子：
{}
答案：
""",
    debug: bool = False,
):
    cl = getClueAIClient(apiKey)  # good without API key
    prompt = prompt_template.format(title)  # shit.
    # generate a prediction for a prompt

    # 如果需要自由调整参数自由采样生成，添加额外参数信息设置方式：generate_config=generate_config
    prediction = cl.generate(
        model_name="clueai-base", prompt=prompt, generate_config=generate_config
    )
    # 需要返回得分的话，指定return_likelihoods="GENERATION"
    output = prediction.generations[0].text
    success = title.strip() != output.strip()
    if debug:
        # print the predicted text
        print("prediction: {}".format(output))
        print("paraphrase success?", success)
    return output, success


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


def paraphraser(
    content: str,
    method: Literal["clueai_free", "cn_nlp_online", "baidu_translator"] = "clueai_free",
    debug: bool = False,
    configs: dict = {},
):  # you could add some translation based methods.
    implementedMethods = ["clueai_free", "cn_nlp_online", "baidu_translator"]
    if method not in implementedMethods:
        raise NotImplementedError("method '%s' not implemented")
    if content.strip() == "":
        return content, True  # to protect paraphrasers.
    try:
        if method == "clueai_free":
            output, success = clueAIParaphraser(content, debug=debug, **configs)
        elif method == "cn_nlp_online":
            output, success = chineseParaphraserAPI(content, debug=debug, **configs)
        elif method == "baidu_translator":
            output, success = baiduParaphraserByTranslation(
                content, debug=debug, **configs
            )
        # you should not be here.
        else:
            raise NotImplementedError("method '%s' not implemented")
        return output, success
    except NotImplementedError as e:
        raise e
    except:
        import traceback

        traceback.print_exc()
        print("Failed to paraphrase content using method '%s'" % method)
        print("Returning original content and failed signal.")
        return content, False


########################[PARAPHRASING]########################
