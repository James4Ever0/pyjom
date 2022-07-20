import translators as ts
# translator = 
# mtranslators = [ts.sogou] #this is pure shit.
# mtranslators = [ts.baidu,ts.sogou]
# mtranslators = [ts.baidu,ts.sogou,ts.iciba]
mtranslators = [ts.youdao,ts.baidu,ts.alibaba] # no yandex, tencent, sogou.
# mtranslators = [ts.baidu,ts.iciba]
import random

def translator(text):
    randomLang = ["zh","zh-CHS"]
    from_language = "en"
    # lang = random.choice(randomLang)
    while True:
        t = random.choice(mtranslators)
        # print(type(translator))

        for rl in randomLang:
            try:
                result = t(text,from_language=from_language,to_language=rl)
                # if len(result) < 3:
                #     print(t)
                #     breakpoint()
                return result
            except:
                import traceback
                traceback.print_exc()