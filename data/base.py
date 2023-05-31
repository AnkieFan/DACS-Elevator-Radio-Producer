import os
import re
import pandas as pd
import lyricsgenius as lg

from nltk import word_tokenize, pos_tag
from nltk.corpus import wordnet, stopwords
from nltk.stem import WordNetLemmatizer


from data import from_billboard
from data import from_spotify

from collections import Counter

api_key = "S4gB5_UF7RN_eQUSIQLhnwtNs3LWB_YZYiosgUeussHWTtIsEEFrJ-ViXkQ5F49X"
genius = lg.Genius(api_key, skip_non_songs=True, excluded_terms=["(Live)"], remove_section_headers=True, timeout=10)


def get_lyrics(title, artist):
    try:
        song = genius.search_song(title=title, artist=artist)
        return song.lyrics
    except Exception as e:
        print(f"There's error when getting lyrcis of '{title}' by {artist}")
        print(str(e))

def store_lyrics(year = None, playlist_id = None) -> None:
    '''
    Get lyrics from Billboard or Spotify playlist and store them in `dataset` folder.
    If 2 args are both None, then it will use the latest Billboard chart.

    '''
    if(playlist_id is None):
        if(year is None or year > 2022 or year < 2006):
            print("Input year is not correct. Now change to the latest one.")
            year = "2022"

        if os.path.exists(f"dataset/{year}"):
            print("We already have the data for this year that can be used.")
            return

        songs = from_billboard.get_top_songs(year)
        folder_name = "2022" if year == None else str(year)
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


def clean(text: str, remove_stopwords=False, stem_words=False) -> list:
    '''
    Return: word tokens without stop words
    '''
    # Empty lyrics
    if type(text) != str or text == '':
        return ''

    text = text.lower()

    if text.endswith("embed"):
        text = text[:-5]

    # Clean the text (here i have 2-3 cases of pre-processing by sampling the data. You might need more)
    text = re.sub("\'s", " ",
                  text)  # we have cases like "Sam is" or "Sam's" (i.e. his) these two cases aren't separable, I choose to compromise are kill "'s" directly
    text = re.sub(" whats ", " what is ", text, flags=re.IGNORECASE)
    text = re.sub("\'ve", " have ", text)

    text = re.sub(" can\'t ", " cannot ", text, flags=re.IGNORECASE)
    text = re.sub(" ain\'t ", " am not ", text, flags=re.IGNORECASE)
    text = re.sub(" tryna ", " try to ", text, flags=re.IGNORECASE)
    text = re.sub(" wanna ", " want to ", text, flags=re.IGNORECASE)
    text = re.sub(" gonna ", " going to ", text, flags=re.IGNORECASE)
    text = re.sub(" \'em ", " them ", text, flags=re.IGNORECASE)

    text = re.sub("n\'t ", " not ", text, flags=re.IGNORECASE)
    text = re.sub(" i\'m ", " i am ", text, flags=re.IGNORECASE)
    text = re.sub("\'re ", " are ", text, flags=re.IGNORECASE)
    text = re.sub("\'ll ", " will ", text, flags=re.IGNORECASE)
    text = re.sub("in\'", "ing", text, flags=re.IGNORECASE)
    text = re.sub(" e - mail ", " email ", text, flags=re.IGNORECASE)
    
    text = re.sub("\\【.*?】+|\\《.*?》+|\\#.*?#+|[.!/_,$&%^*±©≥≤≈()<>+""'?@|:;~{}#]+|[——！\[\]\\\，。=？、：“”‘’`￥……（）《》【】]",
                  ' ', text)
    text = re.sub(r'\$\w*', ' ', text)  # remove entitles
    text = re.sub(re.compile(r'\d'), ' ', text)  # remove numbers
    text = re.sub(r'\s\s+', ' ', text)  # remove extra spaces

    text = word_tokenize(text)

    if (remove_stopwords):
        text = [w for w in text if not w.lower() in stopwords.words('english')]

    if (stem_words):
        text = lemmertize(text)

    # Return a list of words
    return text


def get_wordnet_pos(tag):
    """
    Tool function for lemmatization. Switch the word tag to be `wordnet` tag.
    """
    if tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('R'):
        return wordnet.ADV
    else:
        return None


def lemmertize(words: list[str]):
    tagged_sent = pos_tag(words)
    wnl = WordNetLemmatizer()
    lemmas_sent = []
    for tag in tagged_sent:
        wordnet_pos = get_wordnet_pos(tag[1]) or wordnet.NOUN
        lemmas_sent.append(wnl.lemmatize(tag[0], pos=wordnet_pos))
    return lemmas_sent


def read_cleaned_data(address: str, remove_stopwords=False, stem_words=False) -> dict:
    '''
    Read lyrics from folder and clean them

    Args:
    address(str): the folder name of dataset
    remove_stopwords (boolean): if we remove the stopwords from lyrics. default False
    stem_words (boolean): if we turn the words back to original form. default False

    Return:
    A dictionary with form: {'song name': 'lyrics tokens's}
    '''
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


def store_extraction_result(result: dict, filename: str):
    df = result_dict_to_df(result)
    df.to_csv(f"./result/{filename}", index=False)
    return df


def result_dict_to_df(result: dict) -> pd.DataFrame:
    d = {"name": [], "topic1": [], "topic2": [], "topic3": [], "topic4": [], "topic5": []}
    for key in result.keys():
        if (len(result[key]) != 5): continue

        d["name"].append(key)
        v = result[key]
        for i in range(5):
            d[f"topic{(i + 1)}"].append(v[i][0])
    return pd.DataFrame(d)


def evaluate_c_v(topic_words, tokens):
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

def evaluate(df_5_topics:pd, dic_lyrics_tokens:dict, method = 'u_mass'):
    score = 0
    i = 0
    ran = len(dic_lyrics_tokens)
    for i in range(ran):
        topics_df = df_5_topics.iloc[i].iloc[1:6]
        topics = dataframe_to_list_of_list(topics_df)

        name = list(dic_lyrics_tokens.keys())[i]
        lyrics = dic_lyrics_tokens[name]

        if method == 'u_mass':
            s =  evaluate_u_mass(topics, lyrics)
            score = score + s
            # print(s)

    return round(score/ran,3)


def dataframe_to_list_of_list(df):
    # Convert DataFrame to a list of lists
    result = [df.values.tolist()]

    return result

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

def get_word_vectors(words):
    import gensim

    wv_model = gensim.downloader.load('word2vec-google-news-300')

    word_vector = []
    for key in dict(Counter(words)).keys():
        try:
            word_vector.append(wv_model[key])
        except:
            print(f'word {key} dose not have vector')
            continue
    return word_vector

if __name__ == '__main__':
    from gensim.test.utils import common_corpus, common_dictionary, common_texts
    print(common_texts)

