import os
import re
import pandas as pd
import lyricsgenius as lg
from data import from_billboard
from data import from_spotify

api_key = "S4gB5_UF7RN_eQUSIQLhnwtNs3LWB_YZYiosgUeussHWTtIsEEFrJ-ViXkQ5F49X"
genius = lg.Genius(api_key, skip_non_songs=True, excluded_terms=["(Live)"], remove_section_headers=True, timeout=10)


def get_lyrics(title, artist):
    try:
        song = genius.search_song(title=title, artist=artist)
        return song.lyrics
    except Exception as e:
        print(f"There's error when getting lyrcis of '{title}' by {artist}")
        print(str(e))


def store_lyrics(year=None, playlist_id=None):
    if (playlist_id is None):
        if os.path.exists(f"dataset/{year}"):
            print("We already have the data for this year that can be used.")
            return

        songs = from_billboard.get_top_songs(year)
        folder_name = "current" if year == None else str(year)
    else:
        songs = from_spotify.get_songs(playlist_id=playlist_id)
        folder_name = str(playlist_id)

    try:
        new_folder_path = os.path.join('dataset', folder_name)
        os.makedirs(new_folder_path)
    except FileExistsError:
        pass

    error_df = pd.DataFrame(columns=['Rank', 'Title', 'Artist'])

    for i in range(len(songs)):
        try:
            lyrics = get_lyrics(songs[i].title, songs[i].artist)
            if "\n" in lyrics:
                lines = lyrics.splitlines()
                lyrics = "\n".join(lines[1:])
        except:
            error_df.loc[len(error_df.index)] = [i + 1, songs[i].title, songs[i].artist]
            continue

        name = re.sub(r'[^\w\s]', '', songs[i].title)
        with open(f"dataset/{folder_name}/{i + 1}_{name}.txt", "w", encoding="utf-8") as file:
            file.write(lyrics)

    error_df.to_csv(f"dataset/{folder_name}/0_Errors.csv", index=False, header=True)


def clean(text, remove_stopwords=False, stem_words=False):
    '''
    Return: word tokens without stop words
    '''
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize
    from nltk.stem import SnowballStemmer

    # Empty lyrics
    if type(text) != str or text == '':
        return ''

    text = text.lower()

    # Clean the text (here i have 2-3 cases of pre-processing by sampling the data. You might need more)
    text = re.sub("\'s", " ",
                  text)  # we have cases like "Sam is" or "Sam's" (i.e. his) these two cases aren't separable, I choose to compromise are kill "'s" directly
    text = re.sub(" whats ", " what is ", text, flags=re.IGNORECASE)
    text = re.sub("\'ve", " have ", text)
    text = re.sub(" wanna ", " want to ", text)

    text = re.sub(" can\'t ", " cannot ", text, flags=re.IGNORECASE)
    text = re.sub("n\'t ", " not ", text, flags=re.IGNORECASE)
    text = re.sub(" i\'m ", " i am ", text, flags=re.IGNORECASE)
    text = re.sub("\'re ", " are ", text, flags=re.IGNORECASE)
    text = re.sub("\'ll ", " will ", text, flags=re.IGNORECASE)
    text = re.sub("in\' ", "ing ", text, flags=re.IGNORECASE)
    text = re.sub(" e - mail ", " email ", text, flags=re.IGNORECASE)

    text = re.sub(" a ", " ", text)
    text = re.sub(" an ", " ", text)
    text = re.sub(" the ", " ", text)

    text = re.sub("\\【.*?】+|\\《.*?》+|\\#.*?#+|[.!/_,$&%^*±©≥≤≈()<>+""'?@|:;~{}#]+|[——！\[\]\\\，。=？、：“”‘’`￥……（）《》【】]",
                  ' ', text)
    text = re.sub(r'\$\w*', ' ', text)  # remove entitles
    text = re.sub(re.compile(r'\d'), ' ', text)  # remove numbers
    text = re.sub(r'\s\s+', ' ', text)  # remove extra spaces

    text = word_tokenize(text)

    if (remove_stopwords):
        stopwords = stopwords.words('english')
        text = [w for w in text if not w.lower() in stopwords]

    if (stem_words):
        stemmer = SnowballStemmer('english')
        text = [stemmer.stem(w) for w in text]

    # Return a list of words
    return text


def read_cleaned_data(address, remove_stopwords=False, stem_words=False):
    path = f'dataset/{address}/'
    files = os.listdir(path)
    files.sort()

    lyrics_token = {}

    for file in files:
        with open(path + file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            lines = [clean(text=l, remove_stopwords=remove_stopwords, stem_words=stem_words) for l in lines]
            lines = [l for l in lines if len(l) > 0]
            lyrics_token[file[:-4]] = lines

    return lyrics_token


def evaluate(topic_words, tokens):
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

    dictionary = corpora.Dictionary(tokens)
    corpus = [dictionary.doc2bow(token) for token in tokens]

    cm = CoherenceModel(topics=topic_words,
                        texts=tokens,
                        corpus=corpus,
                        dictionary=dictionary,
                        coherence='c_v')
    coherence = cm.get_coherence()
    return coherence
