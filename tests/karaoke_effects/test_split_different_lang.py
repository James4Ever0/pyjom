# example of TDD.
tests = ["リンの麺は終わった", # only japanese
    "リンの麺は終わった Lina的面吃完了没有", # japanese with chinese containing english
"Lina I miss you Lina我想你了", # english with chinese containing english
"向前冲 冲 冲", # only chinese
"go go go", # chinese containing english (overall)
]
# build a classifier for this? wtf?

# whatlang?

def lastSpaceSpliter():

for test in tests:
