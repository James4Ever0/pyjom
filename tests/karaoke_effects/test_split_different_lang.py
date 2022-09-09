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

from lyrictoolbox import getTextListTranslated

if __name__ == "__main__":
    # result = translate('hello world')
    # print("RESULT:", result)
    # result = translate('hello world', backend='baidu')
    # print("RESULT:", result)
    # exit()
    for test in tests:
        # we need to demostrate this workflow.
        newLyricArray = getTextListTranslated(test)
        print("_________RESULT_________")
        for elem in newLyricArray:
            print(elem)
        print("_________RESULT_________")
