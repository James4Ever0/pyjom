# https://huggingface.co/spacy/en_core_web_sm
# https://medium.com/analytics-vidhya/nlp-essentials-removing-stopwords-and-performing-text-normalization-using-nltk-and-spacy-in-python-2c4024d2e343

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize 
from nltk.stem import PorterStemmer

set(stopwords.words('english'))

text = """He determined to drop his litigation with the monastry, and relinguish his claims to the wood-cuting and 
fishery rihgts at once. He was the more ready to do this becuase the rights had become much less valuable, and he had 
indeed the vaguest idea where the wood and river in question were."""

stop_words = set(stopwords.words('english')) 
  
word_tokens = word_tokenize(text) 
    
filtered_sentence = [] 
  
for w in word_tokens: 
    if w not in stop_words: 
        filtered_sentence.append(w) 

Stem_words = []
ps =PorterStemmer()
for w in filtered_sentence:
    rootWord=ps.stem(w)
    Stem_words.append(rootWord)
print(filtered_sentence)
print(Stem_words)

# from textblob lib import Word method 
from textblob import Word 

text = """He determined to drop his litigation with the monastry, and relinguish his claims to the wood-cuting and 
fishery rihgts at once. He was the more ready to do this becuase the rights had become much less valuable, and he had 
indeed the vaguest idea where the wood and river in question were."""

lem = []
for i in text.split():
    word1 = Word(i).lemmatize("n")
    word2 = Word(word1).lemmatize("v")
    word3 = Word(word2).lemmatize("a")
    lem.append(Word(word3).lemmatize())
print(lem)