import pylrc
from MediaInfo import MediaInfo
from pyonfx import *
from typing import Literal

# wildcard not allowed in function
from pyjom.commons import redisLRUCache

# change the lyric font and font size for hanzi and romaji

import os

os.environ["http_proxy"] = ""
os.environ["https_proxy"] = ""

import string
import zhon.hanzi

englishPuncturals = string.punctuation
chinesePuncturals = zhon.hanzi.punctuation


def removeChinesePunctuation(text):
    for elem in chinesePuncturals:
        text = text.replace(elem, "")
    return text


def removeLeadingAndTrailingPunctuation(text):
    for elem in englishPuncturals + chinesePuncturals:
        if text.startswith(elem):
            text = text[1:]
        if text.endswith(elem):
            if elem == ".":
                continue
            text = text[:-1]
    return text


def removeUnnecessaryPunctuation(text):
    text = removeChinesePunctuation(text)
    text = removeLeadingAndTrailingPunctuation(text)
    return text


def getMusicDuration(musicPath):
    info = MediaInfo(filename=musicPath)  # the music path is not right.
    info = info.getInfo()
    # print(info)
    # breakpoint()
    length = info["duration"]
    length = float(length)
    return length


def lrcToTextArray(musicPath, lrcPath):
    assert lrcPath.endswith(".lrc")
    musicDuration = getMusicDuration(musicPath)

    with open(lrcPath) as lrc_file:
        lrc_string = "".join(lrc_file.readlines())
    # lrc_file.close()

    subs = pylrc.parse(lrc_string)

    lyricDurationThresholds = (0.3, 4)

    textArray = []
    for sub in subs:
        startTime = sub.time
        text = sub.text
        textArray.append((startTime, text))

    textArray.sort(key=lambda x: x[0])

    lastStartTime = textArray[0][0]

    newTextArray = [{"start": textArray[0][0], "text": textArray[0][1]}]

    for startTime, text in textArray[1:]:
        if startTime - lastStartTime < lyricDurationThresholds[0]:
            continue
        else:
            lastStartTime = startTime
            newTextArray.append({"text": text, "start": startTime})

    # now calculate the end time, please?
    # you may want to translate this if you have to.
    # when it does not contains anything in chinese.

    # using deepl?
    # put that aside please? focus on this shit...
    import numpy as np

    lyricDurations = [np.mean(lyricDurationThresholds)]

    for index, elem in enumerate(newTextArray):
        text = elem["text"]
        start = elem["start"]
        nextIndex = index + 1
        if nextIndex < len(newTextArray):
            nextElem = newTextArray[nextIndex]
            nextStart = nextElem["start"]
            end = nextStart - start
            if end > lyricDurationThresholds[0] and end < lyricDurationThresholds[1]:
                lyricDurations.append(end)
            end = min(end, lyricDurationThresholds[1], musicDuration - start) + start
        else:
            end = np.mean(lyricDurations) + start
            end = min(musicDuration, end)
        newTextArray[index].update({"end": end})
    return newTextArray
    # [{'text':text,'start':start,'end':end}, ...]


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


# from loadLingua_pyjnius import pyjniusLinguaDetectLanguageLabel
# from loadLingua_jpype import getLinguaDetectedLanguageLabel as pyjniusLinguaDetectLanguageLabel
def pyjniusLinguaDetectLanguageLabel(text):
    import requests

    url = "http://localhost:{}/langid".format(8978)
    with requests.get(url, params={"text": text}) as r:
        response = r.json()
        if response["code"] == 200:
            return response["result"]
        else:
            print("ERROR WHEN FETCHING LANGUAGE ID")
            print(response)
            breakpoint()


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


def translate(text: str, backend="baidu"):  # deepl is shit. fucking shit.
    # import time
    # time.sleep(delay)
    import requests

    url = "http://localhost:8974/translate"
    mTranslate = lambda text, backend, timeout: requests.get(
        url, params={"backend": backend, "text": text}, timeout=timeout
    )
    backendList = ["deepl", "baidu"]
    if backend == "random":
        import random

        backend = random.choice(backendList)
    assert backend in backendList
    translatedText = text
    if text.strip() == "":
        return text
    try:
        with mTranslate(text, backend, timeout=10) as conn:
            result = conn.json()
            print("TRANSLATOR RESULT:", result)
            if result["code"] == 200:
                translatedText = result["result"]
            else:
                print("SOME ERROR DURING TRANSLATION, PLEASE CHECK SERVER")
            # it just never return.
    except:
        import traceback

        traceback.print_exc()
    return translatedText
    # we know the translator cannot respond the same shit to us right?


def waitForServerUp(port, message, timeout=1):
    import requests

    while True:
        try:
            url = "http://localhost:{}".format(port)
            with requests.get(url, timeout=timeout, proxies=None) as r:
                if type(message) == str:
                    text = r.text.strip('"').strip("'")
                else:
                    text = r.json()
                print("SERVER AT PORT %d RESPONDS:" % port, [text])
                assert text == message
                print("SERVER AT PORT %d IS UP" % port)
                break
        except:
            import traceback

            traceback.print_exc()
            print("SERVER AT PORT %d MIGHT NOT BE UP" % port)
            print("EXPECTED MESSAGE:", [message])
            import time

            time.sleep(1)


waitForServerUp(8974, "unified translator hooked on some clash server")
waitForServerUp(8978, "say hello to jpype fastapi server")
waitForServerUp(8677, "clash update controller", timeout=10)  # probe the clash updator
waitForServerUp(
    8932, {"response": "DFAFilter based Chinese text filter(censor)"}
)  # this is text filter.


def censorTextWithTextFilter(text):
    port = 8932
    import requests

    url = "http://localhost:{}/filter".format(port)
    with requests.get(url, params={"text": text}) as r:
        data = r.json()
        return data["response"]


@redisLRUCache()
def getTextListTranslated(test, translate_method="baidu"):
    newLyricArray = []
    import progressbar

    isBilingual, needToTranslate = getLyricsLanguageType(test)
    if isBilingual:
        for elem in progressbar.progressbar(test):
            text, flag = lastSpaceSpliter(elem)
            if flag:  # splited!
                foreignText, nativeText = text
            else:
                foreignText = text
                nativeText = translate(foreignText, backend=translate_method)
            if foreignText != nativeText:
                newLyricArray.append((foreignText, nativeText))
            else:
                newLyricArray.append((foreignText,))
    else:
        if needToTranslate:
            for elem in progressbar.progressbar(test):
                foreignText = elem
                nativeText = translate(foreignText, backend=translate_method)
                if not nativeText == foreignText:
                    newLyricArray.append((foreignText, nativeText))
                else:
                    newLyricArray.append((foreignText,))
        else:
            newLyricArray = [(elem,) for elem in test.copy()]
    return newLyricArray


def textArrayWithTranslatedListToAss(
    textArray,
    translatedList,
    assPath,
    shiftAdjust=600,
    censor=True,
    puncturalRemoval=True,
    template_path="/root/Desktop/works/pyjom/tests/karaoke_effects/in2.ass.j2",  # but the style. you know.
    # aegisub use system fonts. you pass font name into it.
    ass_template_configs={},
    assStyleConfig={},
    tempdir="/dev/shm/medialang/lyrictoolbox"
    # editly does not support to put the .ass subtitle directly.
):
    defaultStyleConfig = {
        "original": {
            "method": "romaji",
            "style": "Romaji",
            "cutOneByOne": False,
            "charShift": 35,
        },  # this is default. you can change this.
        "translated": {
            "method": "kanji",
            "style": "Kanji",
            "cutOneByOne": True,
            "charShift": 25,  # smaller?
        },
    }
    # newTextArray = [] # dummy shit. must be removed immediately.
    styleConfig = defaultStyleConfig.copy()
    for key in styleConfig.keys():
        styleConfig[key].update(assStyleConfig.get(key, {}))
    import random
    import math
    import jinja2
    from lazero.filesystem.io import readFile

    default_template_configs = {
        "defaultFontname": "Arial",
        "defaultFontsize": 48,  # integer?
        "translationFontname": "Migu 1P",
        "translationFontsize": 48,
        "kanjiFontname": "Migu 1P",
        "kanjiFontsize": 60,  # 46,  # increase. make 'kanji' one char at a time.
        "romajiFontname": "Migu 1P",
        "romajiFontsize": 60,  # 38,  # increase to 60. expand the space!
    }
    mTemplateConfigs = default_template_configs.copy()
    mTemplateConfigs.update(ass_template_configs)

    template = jinja2.Template(source=readFile(template_path))
    template_configured = template.render(**mTemplateConfigs)
    from lazero.filesystem.temp import (
        tmpfile,
        getRandomFileNameUnderDirectoryWithExtension,
    )
    from lazero.filesystem.io import writeFile

    template_configured_savedPath = getRandomFileNameUnderDirectoryWithExtension(
        "ass", tempdir, check=False
    )
    with tmpfile(template_configured_savedPath):
        writeFile(template_configured_savedPath, template_configured)
        io = Ass(template_configured_savedPath, path_output=assPath)
    meta, styles, lines = io.get_data()

    # Creating the star and extracting all the color changes from the input file
    star = Shape.star(5, 4, 10)
    CU = ColorUtility(lines)

    # test this elsewhere. please?

    def romaji(line, l):
        # Setting up a delay, we will use it as duration time of the leadin and leadout effects
        delay = 100
        # Setting up offset variables, we will use them for the \move in leadin and leadout effects
        off_x = 35
        off_y = 15

        # Leadin Effect
        mDelay = 0
        # lastStartTime = line.start_time
        for syl in Utils.all_non_empty(line.syls):
            l.layer = 0
            # l.start_time = syl.end_time
            l.start_time = line.start_time

            # l.start_time = (
            #     line.start_time + 25 * syl.i - delay - 80
            # )  # Remove 80 to start_time to let leadin finish a little bit earlier than the main effect of the first syllable
            # l.end_time = lastStartTime # wtf?
            # lastStartTime = syl.start_time
            l.end_time = syl.start_time
            # l.end_time = line.start_time + syl.start_time # wtf?
            l.dur = l.end_time - l.start_time
            if l.dur <= 0:
                continue

            l.text = (
                "{\\an5\\move(%.3f,%.3f,%.3f,%.3f,0,%d)\\blur2\\t(0,%d,\\blur0)\\fad(%d,0)}%s"
                % (
                    syl.center + math.cos(syl.i / 2) * off_x,
                    syl.middle + math.sin(syl.i / 4) * off_y,
                    syl.center,
                    syl.middle,
                    delay,
                    delay,
                    delay,
                    syl.text,
                )
            )

            io.write_line(l)

        # Main Effect
        for syl in Utils.all_non_empty(line.syls):
            l.layer = 1

            l.start_time = syl.start_time
            # l.start_time = line.start_time + syl.start_time
            l.end_time = syl.end_time + 100
            l.dur = l.end_time - l.start_time

            c1 = "&H81F4FF&"
            c3 = "&H199AAA&"
            # Change color if inline_fx is m1
            if syl.inline_fx == "m1":
                c1 = "&H8282FF&"
                c3 = "&H191AAA&"

            on_inline_effect_2 = ""
            # Apply rotation if inline_fx is m2
            if syl.inline_fx == "m2":
                on_inline_effect_2 = "\\t(0,%d,\\frz%.3f)\\t(%d,%d,\\frz0)" % (
                    l.dur / 4,
                    random.uniform(-40, 40),
                    l.dur / 4,
                    l.dur,
                )

            l.text = (
                "{\\an5\\pos(%.3f,%.3f)%s\\t(0,80,\\fscx105\\fscy105\\1c%s\\3c%s)\\t(80,%d,\\fscx100\\fscy100\\1c%s\\3c%s)}%s"
                % (
                    syl.center,
                    syl.middle,
                    on_inline_effect_2,
                    c1,
                    c3,
                    l.dur - 80,
                    line.styleref.color1,
                    line.styleref.color3,
                    syl.text,
                )
            )

            io.write_line(l)

            # Animating star shape that jumps over the syllables
            # Jump-in to the first syl
            jump_height = 18
            if syl.i == 0:
                FU = FrameUtility(line.start_time - line.leadin / 2, line.start_time)
                for s, e, i, n in FU:
                    l.start_time = s
                    l.end_time = e
                    frame_pct = i / n

                    x = syl.center - syl.width * (1 - frame_pct)
                    y = syl.top - math.sin(frame_pct * math.pi) * jump_height

                    alpha = 255
                    alpha += FU.add(0, syl.duration, -255)
                    alpha = Convert.alpha_dec_to_ass(int(alpha))

                    l.text = (
                        "{\\alpha%s\\pos(%.3f,%.3f)\\bord1\\blur1\\1c%s\\3c%s\\p1}%s"
                        % (alpha, x, y, c1, c3, star)
                    )
                    io.write_line(l)

            # Jump to the next syl or to the end of line
            jump_width = (
                line.syls[syl.i + 1].center - syl.center
                if syl.i != len(line.syls) - 1
                else syl.width
            )
            # FU = FrameUtility(
            #     line.start_time + syl.start_time, line.start_time + syl.end_time
            # )
            FU = FrameUtility(syl.start_time, syl.end_time)
            for s, e, i, n in FU:
                l.start_time = s
                l.end_time = e
                frame_pct = i / n

                x = syl.center + frame_pct * jump_width
                y = syl.top - math.sin(frame_pct * math.pi) * jump_height

                alpha = 0
                # Last jump should fade-out
                if syl.i == len(line.syls) - 1:
                    alpha += FU.add(0, syl.duration, 255)
                alpha = Convert.alpha_dec_to_ass(int(alpha))

                l.text = (
                    "{\\alpha%s\\pos(%.3f,%.3f)\\bord1\\blur1\\1c%s\\3c%s\\p1}%s"
                    % (
                        alpha,
                        x,
                        y,
                        c1,
                        c3,
                        star,
                    )
                )
                io.write_line(l)

        # Leadout Effect
        for syl in Utils.all_non_empty(line.syls):
            l.layer = 0

            l.start_time = syl.end_time
            # l.start_time = line.start_time + syl.end_time + 100
            l.end_time = line.end_time
            # l.end_time = line.end_time - 25 * (len(line.syls) - syl.i) + delay + 100
            # l.end_time = line.end_time - 25 * (len(line.syls) - syl.i) + delay + 100
            l.dur = l.end_time - l.start_time
            if l.dur <= 0:
                continue

            l.text = (
                "{\\an5\\move(%.3f,%.3f,%.3f,%.3f,%d,%d)\\t(%d,%d,\\blur2)\\fad(0,%d)}%s"
                % (
                    syl.center,
                    syl.middle,
                    syl.center + math.cos(syl.i / 2) * off_x,
                    syl.middle + math.sin(syl.i / 4) * off_y,
                    l.dur - delay,
                    l.dur,
                    l.dur - delay,
                    l.dur,
                    delay,
                    syl.text,
                )
            )

            io.write_line(l)

    def kanji(line, l):
        # Setting up a delay, we will use it as duration time of the leadin and leadout effects
        delay = 300
        # Setting up offset variables, we will use them for the \move in leadin and leadout effects
        off_x = 35
        off_y = 15

        # Leadin Effect
        for syl in Utils.all_non_empty(line.syls):
            l.layer = 0
            l.start_time = line.start_time

            # l.start_time = (
            #     line.start_time + 25 * syl.i - delay - 80
            # )  # Remove 80 to start_time to let leadin finish a little bit earlier than the main effect of the first syllable
            l.end_time = syl.start_time
            # l.end_time = line.start_time + syl.start_time
            l.dur = l.end_time - l.start_time
            if l.dur <= 0:
                continue

            l.text = (
                "{\\an5\\move(%.3f,%.3f,%.3f,%.3f,0,%d)\\blur2\\t(0,%d,\\blur0)\\fad(%d,0)}%s"
                % (
                    syl.center + math.cos(syl.i / 2) * off_x,
                    syl.middle + math.sin(syl.i / 4) * off_y,
                    syl.center,
                    syl.middle,
                    delay,
                    delay,
                    delay,
                    syl.text,
                )
            )

            io.write_line(l)

        # Main Effect
        for syl in Utils.all_non_empty(line.syls):
            l.layer = 1

            l.start_time = syl.start_time
            # l.start_time = line.start_time + syl.start_time
            l.end_time = syl.end_time + 100
            l.dur = l.end_time - l.start_time

            c1 = "&H81F4FF&"
            c3 = "&H199AAA&"
            # Change color if effect field is m1
            if line.effect == "m1":
                c1 = "&H8282FF&"
                c3 = "&H191AAA&"

            on_inline_effect_2 = ""
            # Apply rotation if effect field is m2
            if line.effect == "m2":
                on_inline_effect_2 = "\\t(0,%d,\\frz%.3f)\\t(%d,%d,\\frz0)" % (
                    l.dur / 4,
                    random.uniform(-40, 40),
                    l.dur / 4,
                    l.dur,
                )

            l.text = (
                "{\\an5\\pos(%.3f,%.3f)%s\\t(0,80,\\fscx105\\fscy105\\1c%s\\3c%s)\\t(80,%d,\\fscx100\\fscy100\\1c%s\\3c%s)}%s"
                % (
                    syl.center,
                    syl.middle,
                    on_inline_effect_2,
                    c1,
                    c3,
                    l.dur - 80,
                    line.styleref.color1,
                    line.styleref.color3,
                    syl.text,
                )
            )

            io.write_line(l)

        # Leadout Effect
        for syl in Utils.all_non_empty(line.syls):
            l.layer = 0

            l.start_time = syl.end_time + 100
            # l.start_time = line.start_time + syl.end_time + 100
            l.end_time = line.end_time
            # l.end_time = line.end_time - 25 * (len(line.syls) - syl.i) + delay + 100
            l.dur = l.end_time - l.start_time
            if l.dur <= 0:
                continue

            l.text = (
                "{\\an5\\move(%.3f,%.3f,%.3f,%.3f,%d,%d)\\t(%d,%d,\\blur2)\\fad(0,%d)}%s"
                % (
                    syl.center,
                    syl.middle,
                    syl.center + math.cos(syl.i / 2) * off_x,
                    syl.middle + math.sin(syl.i / 4) * off_y,
                    l.dur - delay,
                    l.dur,
                    l.dur - delay,
                    l.dur,
                    delay,
                    syl.text,
                )
            )

            io.write_line(l)

    def sub(line, l):
        # Translation Effect
        l.layer = 0

        l.start_time = line.start_time - line.leadin / 2
        l.end_time = line.end_time + line.leadout / 2
        l.dur = l.end_time - l.start_time

        # Getting interpolated color changes (notice that we do that only after having set up all the times, that's important)
        colors = CU.get_color_change(l)

        # Base text
        l.text = "{\\an5\\pos(%.3f,%.3f)\\fad(%d,%d)}%s" % (
            line.center,
            line.middle,
            line.leadin / 2,
            line.leadout / 2,
            line.text,
        )
        io.write_line(l)

        # Random clipped text colorated
        l.layer = 1
        for i in range(1, int(line.width / 80)):
            x_clip = line.left + random.uniform(0, line.width)
            y_clip = line.top - 5

            clip = (
                x_clip,
                y_clip,
                x_clip + random.uniform(10, 30),
                y_clip + line.height + 10,
            )

            l.text = "{\\an5\\pos(%.3f,%.3f)\\fad(%d,%d)\\clip(%d,%d,%d,%d)%s}%s" % (
                line.center,
                line.middle,
                line.leadin / 2,
                line.leadout / 2,
                clip[0],
                clip[1],
                clip[2],
                clip[3],
                colors,
                line.text,
            )
            io.write_line(l)

    for line in lines:
        # Generating lines
        if line.styleref.alignment >= 7:
            lineModSource = line.copy()
            break
        elif line.styleref.alignment >= 4:  # what is this shit?
            lineModSource = line.copy()
            break
    lineModSourceKanji = lineModSource.copy()
    lineModSourceKanji.style = "Kanji"

    # from test_pylrc import *
    # just a test.
    # censor these lyrics! fucker!
    newTextArray = textArray
    for mIndex, elem in enumerate(newTextArray):
        # if fail then just continue. fuck.
        try:
            translatedTuple = translatedList[mIndex]
            if len(translatedTuple) == 1:
                sourceText = translatedTuple[0]
                translatedText = None
            elif len(translatedTuple) == 2:
                sourceText, translatedText = translatedTuple
            else:
                print("Invalid translatedTuple: %s" % str(translatedTuple))
                breakpoint()
            if sourceText is None or sourceText.strip() == "":
                continue
            else:
                hasTranslatedText = (
                    (translatedText not in [sourceText, None, ""])
                    and type(translatedText) == str
                    and translatedText.strip() != ""
                )
            if puncturalRemoval:
                sourceText = removeUnnecessaryPunctuation(sourceText)
                if hasTranslatedText:
                    translatedText = removeUnnecessaryPunctuation(translatedText)
            if censor:
                sourceText = censorTextWithTextFilter(sourceText)
                if hasTranslatedText:
                    translatedText = censorTextWithTextFilter(translatedText)
            elem["text"] = sourceText

            lineMod = lineModSource.copy()
            lineMod.start_time = max(0, elem["start"] * 1000 - shiftAdjust)
            lineMod.end_time = elem["end"] * 1000 - shiftAdjust
            lineMod.duration = lineMod.end_time - lineMod.start_time
            lineMod.text = elem["text"].strip()
            while True:
                if "  " in lineMod.text:
                    lineMod.text = lineMod.text.replace("  ", " ")
                else:
                    break
            # print(lineMod)
            def addSylToLine(
                lineMod,
                translateShift=0,
                charShift=30,  # increase this!
                CENTER=1600 / 2,
                mSylYShift=600,
                mTop=25,
                mMiddle=49.0,
                mBottom=73.0,
                cutOneByOne=False,
            ):
                lineMod.center = CENTER  # wtf?
                if cutOneByOne:
                    lineMod.words = list(lineMod.text)
                elif lineMod.text.count(" ") >= 1:
                    lineMod.words = lineMod.text.split(" ")
                else:
                    lineMod.words = getJiebaCuttedText(lineMod.text)
                sylList = []

                wordCount = len(lineMod.words)
                if wordCount == 0:  # clean it no matter what.
                    lineMod.words = [" "]
                    lineMod.text = " "
                    wordCount = 1
                sylDuration = (lineMod.end_time - lineMod.start_time) / wordCount
                textLength = len(lineMod.text)

                absWordCenterShiftList = []
                prevWordShift = 0

                wordWidthList = []
                for word in lineMod.words:
                    wordWidth = len(word) * charShift
                    wordWidthList.append(wordWidth)
                    wordLength = len(word) + 1
                    wordCenterShift = (charShift * wordLength) / 2
                    wordShift = charShift * wordLength
                    absWordCenterShift = (
                        CENTER
                        - (textLength * charShift) / 2
                        + prevWordShift
                        + wordCenterShift
                    )
                    absWordCenterShiftList.append(absWordCenterShift)
                    prevWordShift += wordShift
                # CENTER + centerShift*charShift
                getCenter = lambda index: absWordCenterShiftList[index]
                getWidth = lambda index: wordWidthList[index]
                for index, word in enumerate(lineMod.words):
                    syl = Syllable()
                    syl.text = word
                    syl.i = index
                    syl.center = getCenter(index)
                    syl.width = getWidth(index)
                    syl.top = mTop + mSylYShift + translateShift
                    syl.inline_fx = "m2"
                    syl.middle = mMiddle + mSylYShift + translateShift
                    syl.bottom = mBottom + mSylYShift + translateShift
                    syl.start_time = lineMod.start_time + index * sylDuration
                    syl.end_time = syl.start_time + sylDuration
                    syl.duration = sylDuration
                    sylList.append(syl)
                # double check here! fucker
                startSyl = sylList[0]
                startLine = startSyl.center - startSyl.width / 2
                endSyl = sylList[-1]
                endLine = endSyl.center + endSyl.width / 2
                currentCenter = (endLine + startLine) / 2
                # print(startLine, endLine)
                # print('current center:', currentCenter)
                centerShift = int(CENTER - currentCenter)
                # print("CENTERSHIFT", centerShift)
                for index in range(len(sylList)):
                    sylList[index].center += centerShift
                    # import copy
                    # elem = copy.deepcopy(sylList[index])
                    # elem.center = sylList[index].center+centerShift
                    # print("CHANGED CENTER", elem.center, sylList[index].center)
                    # sylList[index] = copy.deepcopy(elem)
                # startSyl = sylList[0]
                # startLine = startSyl.center - startSyl.width/2
                # endSyl = sylList[-1]
                # endLine = endSyl.center + endSyl.width/2
                # currentCenter = (endLine+startLine)/2
                # print(startLine, endLine)
                # print('adjusted center:', currentCenter)

                lineMod.syls = sylList

            # print(lineMod.syls)
            # breakpoint()
            # if translatedText == None:
            #     addSylToLine(lineMod, charShift = 10)
            # else:
            addSylToLine(
                lineMod,
                cutOneByOne=styleConfig["original"]["cutOneByOne"],
                charShift=styleConfig["original"]["charShift"],
            )  # this function is to locate this thing.
            # breakpoint()
            # pyonfx.ass_core.Syllable
            lineMod.style = styleConfig["original"]["style"]
            source = lineMod.copy()
            target = lineMod.copy()
            methodMapping = {"kanji": kanji, "romaji": romaji}
            methodMapping[styleConfig["original"]["method"]](
                source, target
            )  # writing 'kanji' style to romaji?

            if hasTranslatedText:
                # source.style = styleConfig['original']['style']
                lineMod2 = lineMod.copy()
                lineMod2.style = styleConfig["translated"]["style"]
                translatedText = translatedText.replace(" ", "")  # fuck?
                lineMod2.text = translatedText
                translateShift = 100
                addSylToLine(
                    lineMod2,
                    translateShift=translateShift,
                    cutOneByOne=styleConfig["translated"]["cutOneByOne"],
                    charShift=styleConfig["translated"]["charShift"],
                )
                source = lineMod2.copy()
                target = lineMod2.copy()
                # elif line.styleref.alignment >= 4:
                methodMapping[styleConfig["translated"]["method"]](source, target)
            # breakpoint()
            # else:
            #     romaji(source, target)
        except:
            # must be some "start_ms" <= 0 or some shit.
            import traceback

            traceback.print_exc()
            print("Error when generating lyric subtitle line by line.")
            continue
    io.save()
    print("ASS RENDERED AT %s" % assPath)
    return assPath


# do the preview later?
# # io.open_aegisub()
def previewAssWithVideo(sample_video, assPath):
    # from pyonfx import Ass
    # io = Ass(assPath)
    # do not load this shit again unless you want to block the whole shit...
    print("PREVIEWING ASS SCRIPT: %s" % assPath)
    # io.open_mpv(video_path=sample_video) # ain't see shit...
    cmd = "mpv --sub-file='{}' '{}'".format(assPath, sample_video)
    os.system(cmd)


def lrcToAnimatedAss(
    musicPath,
    lrcPath,
    assPath,
    translate=True,
    translate_method: Literal[
        "baidu", "deepl", "random"
    ] = "baidu",  # so how the fuck you can use deepl?
    ass_template_configs={},
    assStyleConfig={},
):
    # already moved to lyrictoolbox
    # TODO: more styles incoming
    textArray = lrcToTextArray(musicPath, lrcPath)
    textList = [elem["text"] for elem in textArray]
    if translate:
        translatedList = getTextListTranslated(
            textList, translate_method=translate_method
        )  # this is taking long time during test. make it redis lru cached!
    else:
        translatedList = [
            (sourceText,) for sourceText in textList
        ]  # notice, we need to examine this damn list.
    # so we pass both arguments to the ass generator.
    return textArrayWithTranslatedListToAss(
        textArray,
        translatedList,
        assPath,
        ass_template_configs=ass_template_configs,
        assStyleConfig=assStyleConfig,
    )


# lyrictoolbox
def getLyricNearbyBpmCandidates(lyric_times, beats):
    nearbys, remains = [], []
    mbeats = beats.copy()
    mbeats = list(set(mbeats))
    mbeats.sort()

    for ltime in lyric_times:
        mbeats.sort(key=lambda x: abs(x - ltime))
        nearby = mbeats[:2].copy()
        nearbys += nearby
        for elem in nearby:
            mbeats.remove(elem)
    remains = mbeats
    return nearbys, remains


# lyrictoolbox
def read_lrc(lrc_path):
    assert lrc_path.endswith(".lrc")
    with open(lrc_path, "r") as f:
        lrc_string = f.read()
        subs = pylrc.parse(lrc_string)
        sublist = []
        for sub in subs:
            time_in_secs = sub.time
            content = sub.text
            sublist.append({"time": time_in_secs, "content": content})
            # another square bracket that could kill me.
        return sublist


# mainly for netease, this may change.
def cleanLrcFromWeb(
    lyric_string: str,
    song_duration: float,
    min_lines_of_lyrics: int = 5,  # whatever. fuck this.
    min_total_lines_of_lyrics: int = 10,
    # potential_forbidden_chars=[], # how to deal with these? just remove the line?
    removeLinesWithPotentialForbiddenChars: bool = True,
    potential_forbidden_chars=["[", "]", "【", "】", "「", "」", "《", "》", "/", "(", ")"],
    core_forbidden_chars=[":", "：", "@"],
):

    import pylrc

    # you'd better inspect the thing. what is really special about the lyric, which can never appear?

    def checkLyricText(text):
        forbidden_chars = core_forbidden_chars
        return not any([char in text for char in forbidden_chars])

    # also get the total time covered by lyric.
    # the time must be long enough, compared to the total time of the song.
    lrc_parsed = pylrc.parse(lyric_string)  # this is string, not None!
    lrc_parsed_list = [line for line in lrc_parsed]
    lrc_parsed_list.sort(key=lambda line: line.time)
    begin = False
    # end = False
    # line_counter = 0
    # new_lines = []
    # lrc_parsed: pylrc.classes.Lyrics
    flags = []
    for line in lrc_parsed_list:
        # print(line)
        text = line.text.strip()
        # startTime = line.time
        if not begin:
            flag = checkLyricText(text)
            if not flag:
                begin = True
        else:
            flag = checkLyricText(text)
            if flag:
                begin = False
        flags.append(flag)
        # breakpoint()

    # select consecutive spans.
    # from test_commons import *
    from pyjom.mathlib import extract_span

    int_flags = [int(flag) for flag in flags]

    mySpans = extract_span(int_flags, target=1)
    print(mySpans)  # this will work.
    # this span is for the range function. no need to add one to the end.

    total_length = 0

    new_lyric_list = []
    for mstart, mend in mySpans:
        length = mend - mstart
        total_length += length
        if length >= min_lines_of_lyrics:
            # process these lines.
            for index in range(mstart, mend):
                line_start_time = lrc_parsed_list[index].time
                line_text = lrc_parsed_list[index].text
                if removeLinesWithPotentialForbiddenChars:
                    if any([char in line_text for char in potential_forbidden_chars]):
                        line_text = ""
                if line_start_time <= song_duration:
                    line_end_time = song_duration
                    if index + 1 < len(lrc_parsed_list):
                        line_end_time = lrc_parsed_list[index + 1].time
                        if line_end_time > song_duration:
                            line_end_time = song_duration
                    new_lyric_list.append((line_text, line_start_time))
                    if index == mend - 1:
                        # append one more thing.
                        new_lyric_list.append(("", line_end_time))
                else:
                    continue
    # for elem in new_lyric_list:
    #     print(elem)
    # exit()

    if total_length >= min_total_lines_of_lyrics:
        print("LYRIC ACCEPTED.")
        new_lrc = pylrc.classes.Lyrics()
        for text, myTime in new_lyric_list:
            timecode_min, timecode_sec = divmod(myTime, 60)
            timecode = "[{:d}:{:.3f}]".format(int(timecode_min), timecode_sec)
            myLine = pylrc.classes.LyricLine(timecode, text)
            new_lrc.append(myLine)
        new_lrc_string = new_lrc.toLRC()
        return new_lrc_string
        # print(new_lrc_string)
        # if nothing returned, you know what to do.


# remerge demanded cut spans.
def remergeDemandedCutSpans(demanded_cut_spans:list[tuple[float,float]],min_span=2, max_span=10):
    new_cut_spans = []  # the last span. could be a problem.
    checkSpanValid = lambda a, b, c: a <= b and a >= c
    continue_flag = 0

    def subdivide_span(
        span_duration, min_span, max_span, span_start, span_end, new_cut_spans,div = 2,
    ):
        
        while True:
            subduration = span_duration / div
            # print(f'div {div} subduation {subduration}')
            # if div>15:
            #     breakpoint()
            if checkSpanValid(subduration, max_span, min_span):
                myspans = [
                    (span_start + i * subduration, span_start + (i + 1) * subduration)
                    for i in range(div)
                ]
                myspans[-1] = (myspans[-1][0], span_end)
                for mspan in myspans:
                    new_cut_spans.append(mspan)
                break
            else:
                div += 1

    for index, span in enumerate(demanded_cut_spans):
        if continue_flag>0:
            continue_flag -=1
            continue
        span_start, span_end = span
        span_duration = span_end - span_start
        if checkSpanValid(span_duration, max_span, min_span):
            new_cut_spans.append((span_start, span_end))
        elif span_duration > max_span:
            subdivide_span(
                span_duration, min_span, max_span, span_start, span_end, new_cut_spans
            )
        elif span_duration < min_span:
            if len(new_cut_spans) > 0:
                # merge with the previous span.
                mynewspan = (new_cut_spans[-1][0], span_end)
                # cut it in the old way.
                new_cut_spans.pop(-1)
            else:
                mynewspan = None
                for i0 in range(0,len(demanded_cut_spans)-index-1):
                    continue_flag +=1
                    mynewspan = span_start, demanded_cut_spans[index + 1+i0][1]
                    if mynewspan[1]-mynewspan[0]>min_span:
                        break
                if mynewspan is None:
                    print('Error!\nMaybe the source cut span list is too small or is some abnormal source cut span.\nPlease check.')
                    breakpoint()
            subdivide_span(
                mynewspan[1]-mynewspan[0],
                min_span,
                max_span,
                mynewspan[0],
                mynewspan[1],
                new_cut_spans,
                div=1
            )
                # new_cut_spans.append(mynewspan)
            # just merge with previous span. if previous span not present, merge with later span.
    return new_cut_spans
