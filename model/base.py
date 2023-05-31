from model import bert_based, tfidf

def get_keywords(lyrics: dict, model = 'bert', n_gram = (1,1), word_no = 5) -> dict:
    keywords = {}
    for key in lyrics.keys():
        if(model == 'bert'): this_keywords = bert_based.get_keybert(lyrics_tokens=lyrics[key], n_gram=n_gram,word_no=word_no)
        elif(model == 'tfidf'): this_keywords = tfidf.get_n_words(lyrics_tokens=lyrics[key], n_gram=n_gram,word_no=word_no)
        else: this_keywords = None
        keywords[key] = this_keywords
        print(f'Song: {key}. Topic: {this_keywords}.')
    return keywords
