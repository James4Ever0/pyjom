# example of TDD.
tests = ["リンの麺は終わった", # only japanese
    "リンの麺は終わった Lina的面吃完了没有", # japanese with chinese containing english
"Lina I miss you Lina我想你了", # english with chinese containing english
"向前冲 冲 冲", # only chinese
"go go go", # chinese containing english (overall)
]
# build a classifier for this? wtf?

# whatlang?

def lastSpaceSpliter(text):
    text = text.strip()
    # index = 0
    for index in range(0, len(text), -1):
        elem = text[index]
        if elem == " ":
            print("LAST SPACE FOUND AT %d", index)
            # do it right now, and return the value here.
            mTuple = (text[0:index], text[index:])
            return mTuple, True
    return text, False # not a list.

for test in tests:
