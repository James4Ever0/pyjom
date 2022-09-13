# https://huggingface.co/spacy/en_core_web_sm
# https://medium.com/analytics-vidhya/nlp-essentials-removing-stopwords-and-performing-text-normalization-using-nltk-and-spacy-in-python-2c4024d2e343

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
# from lazero.utils import inspectObject
from lazero.utils import sprint # print with spliter
# metalazero belongs to lazero package.


import en_core_web_sm

nlp = en_core_web_sm.load()

doc = nlp(
    """He determined to drop his litigation with the monastry, and relinguish his claims to the wood-cuting and fishery rihgts at once. He was the more ready to do this becuase the rights had become much less valuable, and he had indeed the vaguest idea where the wood and river in question were."""
)

# the sentence spliter includes unwanted "\n" char

set(stopwords.words("english"))

stop_words = set([elem.lower() for elem in stopwords.words("english")])

lemma_word1 = []
# this shit has the lang tag. it might be useful for language detection. really?
for token in doc:
    if token.pos_ in ['PRON','CCONJ','ADP','PART','PUNCT','AUX']:
        continue
    if token.text.lower() in stop_words:
        continue
    lemma_word1.append(token.text)
sprint(lemma_word1)  # there is no such -PRON- thing.
# 1st step.

Stem_words = []
ps = PorterStemmer()
for w in lemma_word1:
    rootWord = ps.stem(w)
    Stem_words.append(rootWord)
sprint(Stem_words) # 3rd step

# for reasons that shit can understand.

from sklearn.feature_extraction.text import CountVectorizer


# In[7]:


#把上一步分好词的文本保存为一个txt文档
with open('message.txt','w') as f:
    f.write(words)


# In[8]:


#创建一个CountVectoerizer实例
vect = CountVectorizer()
#打开刚刚保存的txt文档
f = open('message.txt','r')
#使用CountVectorizer拟合数据
vect.fit(f)