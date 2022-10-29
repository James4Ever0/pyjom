text = "Flask的路由,视图和相关配置" # just a sample please?

from nltk.corpus import stopwords
myStopwords = stopwords(['chinese', 'english'])

import jieba.analyse as ana

ana.set_stop_words(myStopwords)

ana.extract_tags