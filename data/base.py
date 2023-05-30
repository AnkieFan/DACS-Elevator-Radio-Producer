import os
import re
import pandas as pd
import lyricsgenius as lg

from nltk import word_tokenize, pos_tag
from nltk.corpus import wordnet, stopwords
from nltk.stem import WordNetLemmatizer

from data import from_billboard
from data import from_spotify

api_key = "S4gB5_UF7RN_eQUSIQLhnwtNs3LWB_YZYiosgUeussHWTtIsEEFrJ-ViXkQ5F49X" 
genius = lg.Genius(api_key, skip_non_songs=True, excluded_terms=["(Live)"], remove_section_headers=True,timeout=10)

def get_lyrics(title, artist):
    try:
        song = genius.search_song(title=title,artist=artist)
        return song.lyrics
    except Exception as e:
        print(f"There's error when getting lyrcis of '{title}' by {artist}")
        print(str(e))

def store_lyrics(year = None, playlist_id = None):
    if(playlist_id is None):
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
    
    # Clean the text (here i have 2-3 cases of pre-processing by sampling the data. You might need more)
    text = re.sub("\'s", " ", text) # we have cases like "Sam is" or "Sam's" (i.e. his) these two cases aren't separable, I choose to compromise are kill "'s" directly
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