from sklearn.feature_extraction.text import TfidfVectorizer

def get_n_words(lyrics_tokens:list[list[str]], n_gram = (1,1), word_no = 5):
    return get_tfidf(lyrics_tokens, n_gram)[:word_no]

def get_tfidf(lyrics_tokens:list[list[str]], n_gram = (1,1)):
    sents = [' '.join(sent) for sent in lyrics_tokens]
    vectorizer = TfidfVectorizer(ngram_range=n_gram)
    X = vectorizer.fit_transform(sents)

    tfidf = {}
    words = vectorizer.get_feature_names_out()
    values = X.toarray().sum(axis=0)
    for i in range(len(words)):
        tfidf[words[i]] = values[i]
    return sorted(tfidf.items(), key=lambda x: x[1], reverse=True)