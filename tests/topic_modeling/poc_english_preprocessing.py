# https://huggingface.co/spacy/en_core_web_sm
# https://medium.com/analytics-vidhya/nlp-essentials-removing-stopwords-and-performing-text-normalization-using-nltk-and-spacy-in-python-2c4024d2e343

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
# from lazero.utils import inspectObject
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
    if token.pos_ in ['PRON']:
        continue
    if token.text.lower() in stop_words:
        continue
    lemma_word1.append(elem)
print(lemma_word1)  # there is no such -PRON- thing.
# 1st step.

Stem_words = []
ps = PorterStemmer()
for w in filtered_sentence:
    rootWord = ps.stem(w)
    Stem_words.append(rootWord)
print(filtered_sentence) # 2nd step
print(Stem_words) # 3rd step