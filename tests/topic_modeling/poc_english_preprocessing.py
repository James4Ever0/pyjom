# https://huggingface.co/spacy/en_core_web_sm
# https://medium.com/analytics-vidhya/nlp-essentials-removing-stopwords-and-performing-text-normalization-using-nltk-and-spacy-in-python-2c4024d2e343

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
# from lazero.utils import inspectObject
# metalazero belongs to lazero package.

set(stopwords.words("english"))

text = """He determined to drop his litigation with the monastry, and relinguish his claims to the wood-cuting and 
fishery rihgts at once. He was the more ready to do this becuase the rights had become much less valuable, and he had 
indeed the vaguest idea where the wood and river in question were."""

stop_words = set(stopwords.words("english"))

word_tokens = word_tokenize(text)

filtered_sentence = []

for w in word_tokens:
    if w not in stop_words:
        filtered_sentence.append(w)

Stem_words = []
ps = PorterStemmer()
for w in filtered_sentence:
    rootWord = ps.stem(w)
    Stem_words.append(rootWord)
print(filtered_sentence) # 2nd step

print(Stem_words) # 3rd step

# from textblob lib import Word method
