text = "Flask的路由,视图和相关配置" # just a sample please?

from nltk.corpus import stopwords
myStopwords = stopwords.words(['chinese', 'english'])

import jieba.analyse as ana
import jieba

text_splited = " ".join(jieba.lcut(text))



tags=ana.extract_tags(text_splited,topK=5,)
print(tags)