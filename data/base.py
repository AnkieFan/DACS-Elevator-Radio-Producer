import os
import re
import pandas as pd
import lyricsgenius as lg

from nltk import word_tokenize, pos_tag
from nltk.corpus import wordnet, stopwords
from nltk.stem import WordNetLemmatizer

from data import from_billboard
from data import from_spotify

api_key = "Your API key"  # TODO: change here
genius = lg.Genius(api_key, skip_non_songs=True, excluded_terms=["(Live)"], remove_section_headers=True,timeout=10)

def get_lyrics(title, artist):
    try:
        song = genius.search_song(title=title,artist=artist)
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
        if(year is None or int(year) > 2022 or int(year) < 2006):
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

    error_df = pd.DataFrame(columns=['Rank','Title','Artist'])

    for i in range(len(songs)):
        try:
            lyrics = get_lyrics(songs[i].title, songs[i].artist)
            if "\n" in lyrics:
                lines = lyrics.splitlines()
                lyrics = "\n".join(lines[1:])
        except:
            error_df.loc[len(error_df.index)] = [i+1, songs[i].title, songs[i].artist]
            continue

        name =  re.sub(r'[^\w\s]', '', songs[i].title)
        with open(f"dataset/{folder_name}/{i+1}_{name}.txt", "w",encoding="utf-8") as file:
            file.write(lyrics)

    error_df.to_csv(f"dataset/{folder_name}/0_Errors.csv",index=False,header=True)

def clean(text:str, remove_stopwords = False, stem_words = False) -> list:
    '''
    Return: word tokens without stop words
    '''
    # Empty lyrics
    if type(text) != str or text=='':
        return ''

    text = text.lower()
    
    if(text.endswith("embed")):
        text = text[:-5]

    # Clean the text (here i have 2-3 cases of pre-processing by sampling the data. You might need more)
    text = re.sub("\'s", " ", text) # we have cases like "Sam is" or "Sam's" (i.e. his) these two cases aren't separable, I choose to compromise are kill "'s" directly
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
    
    text = re.sub("\\【.*?】+|\\《.*?》+|\\#.*?#+|[.!/_,$&%^*±©≥≤≈()<>+""'?@|:;~{}#]+|[——！\[\]\\\，。=？、：“”‘’`￥……（）《》【】]",' ',text)
    text = re.sub(r'\$\w*',' ',text) # remove entitles
    text = re.sub(re.compile(r'\d'),' ',text) # remove numbers
    text = re.sub(r'\s\s+',' ',text) # remove extra spaces

    text = word_tokenize(text) 

    if(remove_stopwords):
        text = [w for w in text if not w.lower() in stopwords.words('english')] 

    if(stem_words):
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
            
def lemmertize(words:list[str]):
    tagged_sent = pos_tag(words)
    wnl = WordNetLemmatizer()
    lemmas_sent = []
    for tag in tagged_sent:
        wordnet_pos = get_wordnet_pos(tag[1]) or wordnet.NOUN
        lemmas_sent.append(wnl.lemmatize(tag[0],pos = wordnet_pos))
    return lemmas_sent

def read_cleaned_data(address:str, remove_stopwords = False, stem_words = False) -> dict:
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
    files= os.listdir(path)
    files.sort()

    lyrics_token = {}

    for file in files:
        with open(path + file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            lines = [clean(text = l, remove_stopwords = remove_stopwords, stem_words=stem_words) for l in lines]
            lines = [l for l in lines if len(l)>0]
            lyrics_token[file[:-4]] = lines
    
    return lyrics_token

def store_extraction_result(result:dict, filename:str):
    df = result_dict_to_df(result)
    df.to_csv(f"./result/{filename}", index=False)
    return df

def result_dict_to_df(result:dict) -> pd.DataFrame:
    d = {"name":[], "topic1":[], "topic2":[], "topic3":[], "topic4":[], "topic5":[]}
    for key in result.keys():
        if(len(result[key])!= 5): continue

        d["name"].append(key)
        v = result[key]
        for i in range(5):
            d[f"topic{(i+1)}"].append(v[i][0])
    return pd.DataFrame(d)