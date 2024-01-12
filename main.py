from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI, SPOTIFY_USERNAME
import os

os.environ["SPOTIPY_CLIENT_ID"] = SPOTIFY_CLIENT_ID
os.environ["SPOTIPY_CLIENT_SECRET"] = SPOTIFY_CLIENT_SECRET
os.environ["SPOTIPY_REDIRECT_URI"] = SPOTIFY_REDIRECT_URI

from bs4 import BeautifulSoup

import spotipy
import requests
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth

# Billboard 100

billboard_date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ") # 2000-08-12
response = requests.get(f"https://www.billboard.com/charts/hot-100/{billboard_date}/")
soup = BeautifulSoup(response.text, "html.parser")
print(soup.prettify())
song_titles = soup.select("li ul li h3")
song_names = [song.getText().strip() for song in song_titles]
print(song_names)

# Spotify API
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri=SPOTIFY_REDIRECT_URI,
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        show_dialog=True,
        cache_path=f".cache-{SPOTIFY_USERNAME}"
    )
)
user_id = sp.current_user()["id"]

#Searching Spotify for songs by title
song_uris = []
year = billboard_date.split("-")[0]
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")
    except UnicodeError:
        print(f"{song} cannot be encoded. Skipped.")

#Creating a new private playlist in Spotify
playlist = sp.user_playlist_create(user=user_id, name=f"{billboard_date} Billboard 100", public=False,description="programatically generated playlist :))")
print(playlist)

#Adding songs found into the new playlist
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)

