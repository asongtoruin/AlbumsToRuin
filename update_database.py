import json

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from colour_puller.album import SpotifyAlbum
from colour_puller.database import AlbumDatabase


auth = spotipy.SpotifyOAuth(
    redirect_uri='http://localhost:8888/callback', username='valeadam'
)

sp = spotipy.Spotify(auth_manager=auth)

recently_played = sp.current_user_recently_played()

recent_albums = []

for item in recently_played['items'][::-1]:
    album = SpotifyAlbum(item['track']['album'])
    if album.art_link and not any(prev == album for prev in recent_albums):
        recent_albums.append(album)

ad = AlbumDatabase()

ad.add_albums(recent_albums)
