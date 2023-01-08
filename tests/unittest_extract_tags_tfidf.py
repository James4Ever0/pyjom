text = "Flask的路由,视图和相关配置"  # just a sample please?

from nltk.corpus import stopwords

myStopwords = stopwords.words(["chinese", "english"])

import jieba.analyse as ana
import jieba

words = jieba.lcut(text)
words_filtered = []
for word in words:
    if word.lower() not in myStopwords:
        words_filtered.append(word)

text_splited = " ".join(words_filtered)

tags = ana.extract_tags(
    text_splited,
    topK=5,
)
print(tags)

# seems like you can only change the source to make it into somewhat solveable problem.
