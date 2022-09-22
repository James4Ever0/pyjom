englishNLP = None
englishStopWords = None
porterStemmer = None


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


def englishTopicModeling(sentences, n_top_words=10, ngram_range=(1, 2),n_components=5):
    dataList = []
    for sentence in sentences:
        for x in "\n\r\t":
            sentence = sentence.replace(x, "")
        sentence = sentence.strip()
        row = englishSentencePreprocessing(sentence)
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

def chineseSentencePreprocessing(sentence):
    import jieba
    words=jieba.lcut(sentence)
    for word in words:
        

def chineseTopicModeling(sentences, n_top_words=10, ngram_range=(1, 2),n_components=5):
    dataList = []
    for sentence in sentences:
        for x in "\n\r\t":
            sentence = sentence.replace(x, "")
        sentence = sentence.strip()
        row = englishSentencePreprocessing(sentence)
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
