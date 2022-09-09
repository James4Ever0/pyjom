# example of TDD.
import os

# os.environ['http_proxy'] = ""
# os.environ['https_proxy'] = ""
# os.environ['all_proxy'] = ""

tests = [
    ["リンの麺は終わった", "リンの麺は終わった"],
    # only japanese
    [
        "リンの麺は終わった Lina的面吃完了没有",
        "リンの麺は終わった Lina的面吃完了没有",
    ],  # japanese with chinese containing english
    [
        "Lina I miss you Lina我想你了",
        "Lina I miss you Lina我想你了",
    ],  # english with chinese containing english
    ["向前冲 冲 冲", "向前冲 冲 冲"],  # only chinese
    ["go go go", "go go go"],  # chinese containing english (overall)
]
# build a classifier for this? wtf?

# whatlang?


def lastSpaceSpliter(text):
    text = text.strip()
    # index = 0
    for index in range(len(text) - 1, -1, -1):
        # print(index)
        elem = text[index]
        if elem == " ":
            print("LAST SPACE FOUND AT %d", index)
            # do it right now, and return the value here.
            mTuple = (text[0:index].strip(), text[index:].strip())
            return mTuple, True
    return text, False  # not a list.


# if there is a single shit failed to pass this 'lastSpaceSpliter' test, this is not a bilingual lrc file from netease.


def getJiebaCuttedText(text):
    import jieba

    textList = jieba.lcut(text)
    textList = [elem.strip() for elem in textList]
    textList = [elem for elem in textList if len(elem) > 0]
    return textList


from loadLingua_pyjnius import pyjniusLinguaDetectLanguageLabel

nativeLangFlagStandard = "CHINESE"

# need to make this thing totally bilingual if we have to.

# for test in tests:
def getLyricsLanguageType(test):
    isBilingual = False
    needToTranslate = True  # not useful for our bilingual shit.
    print("_______________TEST SUBJECT_______________")
    for elem in test:
        print(elem)
    print("_______________TEST SUBJECT_______________")
    flags = [int(flag) for _, flag in [lastSpaceSpliter(elem) for elem in test]]
    print(flags)
    if sum(flags) < len(flags) * 0.8:
        print("NOT A BILIGUAL LYRICS FILE")
    else:
        # having the potential of being a bilingual shit.
        # process this shit separately.
        # double check if this is really bilingual.
        foreignLangList = []
        nativeLangList = []
        for elem in test:
            text, flag = lastSpaceSpliter(elem)
            if flag:
                # this line might be bilingual.
                foreignLang, nativeLang = text
                foreignLangList.append(foreignLang)
                nativeLangList.append(nativeLang)
        foreignLangString = " ".join(foreignLangList)
        nativeLangString = " ".join(nativeLangList)

        # import whatlang
        # nativeLangFlagStandard = "Cmn"
        # foreignLangFlag = whatlang.detect_language(foreignLangString)
        # nativeLangFlag = whatlang.detect_language(nativeLangString)

        # import cld3
        # nativeLangFlagStandard = "zh"
        # foreignLangFlag = cld3.get_language(foreignLangString)
        # nativeLangFlag = cld3.get_language(nativeLangString)

        # from textblob import TextBlob
        # nativeLangFlagStandard = "zh"
        # foreignLangFlag = TextBlob(foreignLangString).detect_language()
        # nativeLangFlag = TextBlob(nativeLangString).detect_language()

        # import langid
        # nativeLangFlagStandard = "zh"
        # foreignLangFlag = langid.classify(foreignLangString)
        # nativeLangFlag = langid.classify(nativeLangString)

        foreignLangFlag = (pyjniusLinguaDetectLanguageLabel(foreignLangString), 1)
        nativeLangFlag = (pyjniusLinguaDetectLanguageLabel(nativeLangString), 1)
        # there's no probability out there! WTF?

        print(foreignLangFlag)
        print(nativeLangFlag)
        # breakpoint()
        if (
            foreignLangFlag[0] != nativeLangFlagStandard
            and nativeLangFlag[0] == nativeLangFlagStandard
        ):
            # this is for sure the bilingual shit.
            isBilingual = True
            print("BILINGUAL LYRIC FILE IDENTIFIED.")
            # then? how shall we judge this?
            # let the jieba.lcut to handle the cutting. please?
            # remove all blanks in the list.
        else:
            print("NOT A BILIGUAL LYRICS FILE")
    # what you are going to do with this shit?
    if not isBilingual:
        print("checking main language")
        lyricString = " ".join(test)
        mainLanguage = pyjniusLinguaDetectLanguageLabel(lyricString)
        print("main language id:", mainLanguage)
        if mainLanguage == nativeLangFlagStandard:
            print("no need to translate")
            needToTranslate = False
        else:
            print("need to translate")
    return isBilingual, needToTranslate


def translate(text, backend="deepl"):
    assert backend in ["deepl", "baidu"]
    if backend == "deepl":
        import requests
        port = 8281
        # env ROCKET_PORT=8281 ./executable_deepl
        url = "http://localhost:{}/translate".format(port)
        data = {"text": text, "source_lang": "auto", "target_lang": "ZH"}
        r = requests.post(url, json=data)
        response = r.json()
        code = response['code']
        if code == 200:
            return response['data']
        else:
            print("DEEPL RESPONSE ERROR. PLEASE CHECK")
            print(response)
            breakpoint()
        # print(response)
    elif backend == 'baidu':
        # use paddlehub.
        language_translation_model = hub.Module(name='baidu_translate')
        language_recognition_model = hub.Module(name='baidu_language_recognition')
        
        # where is the damn code?


if __name__ == "__main__":
    result = translate('hello world')
    print("RESULT:", result)
    result = translate('hello world', backend='baidu')
    print("RESULT:", result)
    exit()
    for test in tests:
        # we need to demostrate this workflow.
        newLyricArray = []
        isBilingual, needToTranslate = getLyricsLanguageType(test)
        if isBilingual:
            for elem in test:
                text, flag = lastSpaceSpliter(elem)
                if flag:  # splited!
                    foreignText, nativeText = text
                else:
                    foreignText = text
                    nativeText = translate(foreignText)
                newLyricArray.append((foreignText, nativeText))
        else:
            if needToTranslate:
                for elem in test:
                    foreignText = elem
                    nativeText = translate(foreignText)
                    newLyricArray.append((foreignText, nativeText))
                else:
                    newLyricArray = test.copy()
