import os

import spotipy
from dotenvy import load_env
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
import spotipy.util as util
import dotenv
# create variables for spotify authentication


load_env(".env")
cid = os.getenv("CID")
secret = os.getenv("SECRET")
redirect_uri = 'http://localhost/'

credManager = SpotifyClientCredentials(cid, secret)
#sp = spotipy.Spotify(client_credential_manager=credManager)
sp = spotipy.oauth2.SpotifyOAuth(cid, secret, redirect_uri)

username = 'wvlyrhu0u1141lcnyxikbg5re'
scope = 'user-library-read'
token = util.prompt_for_user_token(username, scope, client_id=cid, client_secret=secret,
                                   redirect_uri=redirect_uri)

class GetUrls:
    def __init__(self):
        pass

    def getPlaylistNames(self):
        if token:
            names = []
            sp = spotipy.Spotify(auth=token)
            results = sp.current_user_playlists()
            for item in results['items']:
                name = item['name']
                names.append(name)
            return names



    def getUrls(self):
        if token:
            urls = []
            sp = spotipy.Spotify(auth=token)
            results = sp.current_user_playlists()
            for item in results['items']:
                url = item['external_urls']['spotify']
                urls.append(url)
        return urls


if __name__ == '__main__':
    
    username = '4wrYLspvSO21PHoYuUsEig&nd'
    scope = 'user-library-read'
    token = util.prompt_for_user_token(username, scope, client_id=cid, client_secret=secret, redirect_uri=redirect_uri)

    if token:
        sp = spotipy.Spotify(auth=token)
        results = sp.current_user_saved_tracks()
        print(results)
    else:
        print("failed")

    if token:
        sp = spotipy.Spotify(auth=token)
        results = sp.current_user_playlists()
        for item in results['items']:
            url = item['external_urls']
            print(url['spotify'])
    else:
        print("can't get token for user")
