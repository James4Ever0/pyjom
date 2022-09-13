# https://huggingface.co/spacy/en_core_web_sm
# https://medium.com/analytics-vidhya/nlp-essentials-removing-stopwords-and-performing-text-normalization-using-nltk-and-spacy-in-python-2c4024d2e343

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from metalazero import inspectObject

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
print(filtered_sentence)
print(Stem_words)

# from textblob lib import Word method
# if textblobTest:
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

import en_core_web_sm

nlp = en_core_web_sm.load()

doc = nlp(
    """He determined to drop his litigation with the monastry, and relinguish his claims to the wood-cuting and fishery rihgts at once. He was the more ready to do this becuase the rights had become much less valuable, and he had indeed the vaguest idea where the wood and river in question were."""
)

# the sentence spliter includes unwanted "\n" char

lemma_word1 = []
# this shit has the lang tag. it might be useful for language detection. really?
for token in doc:
    # print("LEMMA", token.lemma_)
    # not reliable.
    # ['ancestors', 'check_flag', 'children', 'cluster', 'conjuncts', 'dep', 'dep_', 'doc', 'ent_id', 'ent_id_', 'ent_iob', 'ent_iob_', 'ent_kb_id', 'ent_kb_id_', 'ent_type', 'ent_type_', 'get_extension', 'has_dep', 'has_extension', 'has_head', 'has_morph', 'has_vector', 'head', 'i', 'idx', 'iob_strings', 'is_alpha', 'is_ancestor', 'is_ascii', 'is_bracket', 'is_currency', 'is_digit', 'is_left_punct', 'is_lower', 'is_oov', 'is_punct', 'is_quote', 'is_right_punct', 'is_sent_end', 'is_sent_start', 'is_space', 'is_stop', 'is_title', 'is_upper', 'lang', 'lang_', 'left_edge', 'lefts', 'lemma', 'lemma_', 'lex', 'lex_id', 'like_email', 'like_num', 'like_url', 'lower', 'lower_', 'morph', 'n_lefts', 'n_rights', 'nbor', 'norm', 'norm_', 'orth', 'orth_', 'pos', 'pos_', 'prefix', 'prefix_', 'prob', 'rank', 'remove_extension', 'right_edge', 'rights', 'sent', 'sent_start', 'sentiment', 'set_extension', 'set_morph', 'shape', 'shape_', 'similarity', 'subtree', 'suffix', 'suffix_', 'tag', 'tag_', 'tensor', 'text', 'text_with_ws', 'vector', 'vector_norm', 'vocab', 'whitespace_']
    # print(dir(token))
    # breakpoint()
    lemma_word1.append(token.lemma_)
print(lemma_word1)  # there is no such -PRON- thing.
