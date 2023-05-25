import os
import re
import pandas as pd
import lyricsgenius as lg
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
