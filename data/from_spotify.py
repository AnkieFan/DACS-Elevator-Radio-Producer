import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_id = "Your Client ID"
client_secret = "Your Client Secret"
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

class Song():
    def __init__(self, title, artist) -> None:
        self.title = title
        self.artist = artist

def get_songs(playlist_id):
    songs = []
    l = sp.playlist_items(playlist_id=playlist_id)['items']
    for each in l:
        try:
            songs.append(Song(title = each['track']['name'], artist = each['track']['artists'][0]['name']))
        except Exception as e:
            print(str(e))
            print(f"There's error when getting lyrcis of '{each['track']['name']}'")
    return songs
