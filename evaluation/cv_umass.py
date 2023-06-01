import pandas as pd


def evaluate(df_5_topics: pd, dic_lyrics_tokens: dict, method='u_mass'):
    score = 0
    i = 0
    ran = len(dic_lyrics_tokens)
    for i in range(ran):
        topics_df = df_5_topics.iloc[i].iloc[1:6]
        topics = dataframe_to_list_of_list(topics_df)

        name = list(dic_lyrics_tokens.keys())[i]
        lyrics = dic_lyrics_tokens[name]

        if method == 'u_mass':
            s = evaluate_u_mass(topics, lyrics)
            score = score + s
            # print(s)
        elif method == 'c_v':
            s = evaluate_c_v(topics, lyrics)
            score = score + s

    return round(score / ran, 4)


def dataframe_to_list_of_list(df):
    # Convert DataFrame to a list of lists
    result = [df.values.tolist()]

    return result


def evaluate_c_v(topic_words, texts):
    """
    Evaluate the performance using C_V,
        a combined metric of
        normalized pointwise mutual information (NPMI)
        and cosine similarity (Mifrah and Benlahmar, 2020).
    The gensim.models.coherencemodel is called with topics,
        texts, corpus, dictionary and coherence with 'c_v' in our model.
    The higher the score of the C_V, the more understandable a topic can be to a human.

    :param topic_words: Topics in List.
        format: topic_words = [
        ['human', 'computer', 'system', 'interface'],
        ['graph', 'minors', 'trees', 'eps']
        ]
    :param tokens: Tokenized texts, needed for coherence models
        that use sliding window based (i.e. coherence=`c_something`)
        probability estimator.
    :return: coherence
    """
    import gensim.corpora as corpora
    from gensim.models.coherencemodel import CoherenceModel
    from gensim.corpora.dictionary import Dictionary
    dic = Dictionary(texts)
    corpus = [dic.doc2bow(text) for text in texts]

    cm = CoherenceModel(topics=topic_words,
                        texts=texts,
                        corpus=corpus,
                        dictionary=dic,
                        coherence='c_v')
    coherence = cm.get_coherence()
    return coherence


def evaluate_u_mass(topic_words, texts):
    """
    Evaluate the performance using u_mass,
        a combined metric of
        document co-occurrence counts,
        one-preceding segmentation,
        and a logarithmic conditional probability as a confirmation measure (Mifrah and Benlahmar, 2020).
    The gensim.models.coherencemodel is called with topics,
        corpus, dictionary and coherence with 'u_mass' in our model.
    The closer the score is to 0, the more understandable a topic can be to a human.

    :param topic_words: Topics in List.
        format: topic_words = [
        ['human', 'computer', 'system', 'interface'],
        ['graph', 'minors', 'trees', 'eps']
        ]
    :return: coherence
    """
    from gensim.models.coherencemodel import CoherenceModel
    from gensim.corpora.dictionary import Dictionary
    dic = Dictionary(texts)
    corpus = [dic.doc2bow(text) for text in texts]

    cm = CoherenceModel(topics=topic_words,
                        corpus=corpus,
                        dictionary=dic,
                        coherence='u_mass')
    coherence = cm.get_coherence()
    return coherence


def evaluate_topic_songname_similarity():
    from sklearn.metrics.pairwise import cosine_similarity

    evaluation = 0

    return evaluation
