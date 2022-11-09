from reloading import reloading
englishNLP = None
englishStopWords = None
porterStemmer = None


@reloading
def get_topics(model, feature_names, n_top_words):
    # 首先是遍历模型中存储的话题序号和话题内容
    topics = []
    for topic_idx, topic in enumerate(model.components_):
        # 然后打印话题的序号以及指定数量的最高频的关键词
        message = "topic #%d:" % topic_idx
        mList = [feature_names[i] for i in topic.argsort()[: -n_top_words - 1 : -1]]
        mListStr = " ".join(mList)
        message += mListStr
        mSet = set(mList)  # the set contains word groups like 'river question'
        cDict = {k: mList.count(k) for k in mSet}
        mRealList = mListStr.split(" ")
        mRealList = [
            x.strip() for x in mRealList if len(x.strip()) > 1
        ]  # usually things shorter than 2 letters are no good.
        mRealSet = set(mRealList)
        cRealDict = {k: mRealList.count(k) for k in mRealSet}
        topics.append({"combined": mList, "separate": mRealList})
    return topics


@reloading
def print_topics(model, feature_names, n_top_words):
    # 首先是遍历模型中存储的话题序号和话题内容
    for topic_idx, topic in enumerate(model.components_):
        # 然后打印话题的序号以及指定数量的最高频的关键词
        message = "topic #%d:" % topic_idx
        mList = [feature_names[i] for i in topic.argsort()[: -n_top_words - 1 : -1]]
        mListStr = " ".join(mList)
        message += mListStr
        mSet = set(mList)  # the set contains word groups like 'river question'
        cDict = {k: mList.count(k) for k in mSet}
        mRealList = mListStr.split(" ")
        mRealList = [
            x.strip() for x in mRealList if len(x.strip()) > 1
        ]  # usually things shorter than 2 letters are no good.
        mRealSet = set(mRealList)
        cRealDict = {k: mRealList.count(k) for k in mRealSet}

        print("MESSAGE", message)
        print("SET", mSet)
        print("COUNT DICT", cDict)  # pointless to count here?
        print("RealSET", mRealSet)
        print("RealCOUNT DICT", cRealDict)
    print()


@reloading
def englishSentencePreprocessing(
    text, unwantedPOS=["PRON", "CCONJ", "ADP", "PART", "PUNCT", "AUX"]
):
    global englishNLP, englishStopWords, porterStemmer
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize
    import en_core_web_sm
    from nltk.stem import PorterStemmer

    if englishNLP is None:
        englishNLP = en_core_web_sm.load()
    doc = englishNLP(text)
    if englishStopWords is None:
        set(stopwords.words("english"))
        englishStopWords = set([elem.lower() for elem in stopwords.words("english")])
    if porterStemmer is None:
        porterStemmer = PorterStemmer()
    lemma_word1 = []
    # this shit has the lang tag. it might be useful for language detection. really?
    for token in doc:
        if token.pos_ in unwantedPOS:
            continue
        if token.text.lower() in englishStopWords:
            continue
        lemma_word1.append(token.text)

    Stem_words = []
    for w in lemma_word1:
        rootWord = porterStemmer.stem(w)
        Stem_words.append(rootWord)
    return Stem_words

@reloading
def sentenceFlatten(sentence, padding = " "):
    assert len(padding) == 1
    assert type(padding) == str
    for x in "\n\r\t":
        sentence = sentence.replace(x, padding)
    while True:
        if padding*2 in sentence:
            sentence = sentence.replace(padding*2, padding)
        else:
            break
    sentence = sentence.strip()
    return sentence

@reloading
def englishTopicModeling(sentences, n_top_words=10, ngram_range=(1, 2),n_components=5):
    dataList = []
    for sentence in sentences:
        sentence = sentenceFlatten(sentence)
        row = englishSentencePreprocessing(sentence)
        if len(row)>0:
            elem = " ".join(row)
            dataList.append(elem)

    data = "\n".join(dataList)

    from sklearn.feature_extraction.text import TfidfVectorizer

    # 创建一个CountVectoerizer实例
    tfidf = TfidfVectorizer(ngram_range=ngram_range)
    # 打开刚刚保存的txt文档
    from io import StringIO

    f = StringIO(data)
    # 使用CountVectorizer拟合数据
    x_train = tfidf.fit_transform(f)

    from sklearn.decomposition import LatentDirichletAllocation

    lda = LatentDirichletAllocation(n_components=n_components)
    lda.fit(x_train)

    topics = get_topics(lda, tfidf.get_feature_names(), n_top_words)
    return topics

from functools import lru_cache
from lazero.utils.logger import traceError
# import os
@lru_cache(maxsize=1)
def getChineseStopWords(stopwordFileList = ["/root/Desktop/works/pyjom/tests/stopwords/chinese_stopwords.txt","/root/Desktop/works/pyjom/tests/stopwords/stopwords-zh/stopwords-zh.json"]):
    import json
    stopwords = []
    for filename in stopwordFileList:
        # if os.path.exists(filename) and os.path.isfile(filename):
        try:
            with open(filename,'r') as f:
                content = f.read()
            if filename.endswith('.json'):
                try:
                    mList = json.loads(content)
                    assert type(mList) == list
                    stopwords+=mList
                except:
                    traceError(_breakpoint=True)
            else:
                mList = content.split("\n")
                mList = [x.replace("\n",'').strip() for x in mList]
                mList = [x for x in mList if len(x)>0]
                stopwords+=mList
        except:
            traceError(_breakpoint=True)
    return list(set(stopwords))


@reloading
def chineseSentencePreprocessing(sentence):
    import jieba
    import string
    from zhon.hanzi import punctuation
    chinese_stopwords = getChineseStopWords()
    words=jieba.lcut(sentence)
    rows = []
    for word in words:
        word = word.strip()
        if word in punctuation:
            continue
        elif word in string.punctuation:
            continue
        elif word in chinese_stopwords:
            continue
        rows.append(word)
    return rows


@reloading
def chineseTopicModeling(sentences, n_top_words=10, ngram_range=(1, 2),n_components=5):
    dataList = []
    for sentence in sentences:
        sentence = sentenceFlatten(sentence)
        row = chineseSentencePreprocessing(sentence)
        if len(row)>0:
            elem = " ".join(row)
            dataList.append(elem)

    data = "\n".join(dataList)

    from sklearn.feature_extraction.text import TfidfVectorizer

    # 创建一个CountVectoerizer实例
    tfidf = TfidfVectorizer(ngram_range=ngram_range)
    # 打开刚刚保存的txt文档
    from io import StringIO

    f = StringIO(data)
    # 使用CountVectorizer拟合数据
    x_train = tfidf.fit_transform(f)

    from sklearn.decomposition import LatentDirichletAllocation

    lda = LatentDirichletAllocation(n_components=n_components)
    lda.fit(x_train)

    topics = get_topics(lda, tfidf.get_feature_names(), n_top_words)
    return topics
