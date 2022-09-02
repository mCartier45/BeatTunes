import spotipy
from spotipy import *
from spotipy.oauth2 import SpotifyClientCredentials

if __name__ == '__main__':
    cid = 'a4d934e4e20c4eabba2aa6240c13cba4'
    secret = 'd0815c59eb194a009b0cbeb6fb9a4e64'

    credManager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
    sp = spotipy.Spotify(client_credentials_manager=credManager)

    results = sp.audio_analysis('spotify:track:6rqhFgbbKwnb9MLmUQDhG6')

    print(results)
