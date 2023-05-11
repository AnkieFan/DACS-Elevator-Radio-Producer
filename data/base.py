import os
import re
import pandas as pd
import billboard
import lyricsgenius as lg

api_key = "S4gB5_UF7RN_eQUSIQLhnwtNs3LWB_YZYiosgUeussHWTtIsEEFrJ-ViXkQ5F49X" 
genius = lg.Genius(api_key, skip_non_songs=True, excluded_terms=["(Remix)", "(Live)"], remove_section_headers=True)

def get_top_songs(year = None):
    if(year != None and (year >= 2023 or year <2006)):
        print("The min and max supported years for the 'hot-100-songs' chart are 2006 and 2022, respectively.")
        year = None
    
    chart = billboard.ChartData('hot-100-songs', year = year)
    return chart

def get_lyrics(title, artist):
    try:
        song = genius.search_song(title=title,artist=artist)
        return song.lyrics
    except Exception as e:
        print(f"There's error when getting lyrcis of '{title}' by {artist}")
        print(str(e))

def store_data(year = None):
    chart = get_top_songs(year)
    year = "current" if year == None else str(year)

    try:
        new_folder_path = os.path.join('dataset', year)
        os.makedirs(new_folder_path)
    except FileExistsError:
        pass

    error_df = pd.DataFrame(columns=['Rank','Title','Artist'])

    for i in range(len(chart)):
        try:
            lyrics = get_lyrics(chart[i].title, chart[i].artist)
            if "\n" in lyrics:
                lines = lyrics.splitlines()
                lyrics = "\n".join(lines[1:])
        except:
            error_df.loc[len(error_df.index)] = [i+1, chart[i].title, chart[i].artist]
            continue

        name =  re.sub(r'[^\w\s]', '', chart[i].title)
        with open(f"dataset/{year}/{i+1}_{name}.txt", "w",encoding="utf-8") as file:
            file.write(lyrics)

    error_df.to_csv(f"dataset/{year}/0_Errors.csv",index=False,header=True)
    
if __name__ == "__main__":
    store_data(2020)
