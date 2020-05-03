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

# Get counts
queue = ad.count_records(status='queued')
completed = ad.count_records(status='completed')
errors = ad.count_records(status='error')

# Draw onto inky display if connected, but don't error the whole process if 
# there are library issues (e.g. GPIO permissions)
try:
    from inky import InkyPHAT
    from .dashboard import draw_dashboard

    inky_display = InkyPHAT('red')

    img = draw_dashboard(queue, completed, errors)

    inky_display.set_image(img.rotate(180))
finally:
    pass