def englishSentencePreprocessing():

def englishTopicModeling(n_top_words = 10):
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize
    from nltk.stem import PorterStemmer

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
        if token.pos_ in ["PRON", "CCONJ", "ADP", "PART", "PUNCT", "AUX"]:
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
    sprint(Stem_words)  # 3rd step

    Stem_words += ((len(Stem_words) - 1) % 5) * [""]  # padding

    import numpy as np

    Stem_words = np.array(Stem_words)
    Stem_words = Stem_words.reshape(5, -1)
    # sprint(Stem_words)
    # row, col = Stem_words.shape
    # exit()
    # for reasons that shit can understand.
    # np.nditer is for iteration over every elem
    dataList = []
    for row in Stem_words:
        # print(row)
        elem = " ".join(row)
        dataList.append(elem)

    data = "\n".join(dataList)

    from sklearn.feature_extraction.text import TfidfVectorizer

    # In[8]:

    # 创建一个CountVectoerizer实例
    tfidf = TfidfVectorizer(ngram_range=(1, 2))
    # 打开刚刚保存的txt文档
    from io import StringIO
    f = StringIO(data)
    # 使用CountVectorizer拟合数据
    x_train = tfidf.fit_transform(f)

    from sklearn.decomposition import LatentDirichletAllocation

    lda = LatentDirichletAllocation(n_components=5)
    lda.fit(x_train)

    def print_topics(model, feature_names, n_top_words):
        # 首先是遍历模型中存储的话题序号和话题内容
        for topic_idx, topic in enumerate(model.components_):
            # 然后打印话题的序号以及指定数量的最高频的关键词
            message = "topic #%d:" % topic_idx
            mList = [feature_names[i] for i in topic.argsort()[: -n_top_words - 1 : -1]]
            mListStr = " ".join(
                mList
            )
            message += mListStr
            mSet  = set(mList) # the set contains word groups like 'river question'
            cDict = {k:mList.count(k) for k in mSet}
            mRealList = mListStr.split(" ")
            mRealList = [x.strip() for x in mRealList if len(x.strip()) > 1] # usually things shorter than 2 letters are no good.
            mRealSet = set(mRealList)
            cRealDict = {k:mRealList.count(k) for k in mRealSet}

            print("MESSAGE",message)
            print("SET", mSet)
            print("COUNT DICT", cDict) # pointless to count here?
            print("RealSET", mRealSet)
            print("RealCOUNT DICT", cRealDict)
        print()


    print_topics(lda, tfidf.get_feature_names(), n_top_words)