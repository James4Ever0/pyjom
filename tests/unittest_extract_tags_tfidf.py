text = "Flask的路由,视图和相关配置" # just a sample please?

from nltk.corpus import stopwords
myStopwords = stopwords(['chinese', 'english'])

import jieba.analyse as ana
import jieba

text_splited = " ".join(jieba.lcut(text))

ana.set_stop_words(myStopwords)
tags=ana.extract_tags(text_splited,topK=5,)
print(tags)