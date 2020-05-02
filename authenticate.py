import spotipy.util as util

token = util.prompt_for_user_token(
    'valeadam', scope='user-read-recently-played', 
    redirect_uri='http://localhost:8888/callback'
)