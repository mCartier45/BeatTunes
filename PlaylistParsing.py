import os
import webbrowser
from urllib.parse import urlencode

import requests
import spotipy
from dotenv import load_dotenv
from spotipy import SpotifyClientCredentials, SpotifyOAuth


class PlaylistProcessor:
    base_url = "https://api.spotify.com/v1"

    load_dotenv()
    cid = os.getenv("CID")
    secret = os.getenv("SECRET")

    HEADERS = {"client_id": cid,
               "client_secret": secret,
               "response_type": "code",
               "redirect_uri": "http://localhost/",
               "scope": "user-library-read"}

    def __init__(self):
        load_dotenv()
        self.make_init_request()

    def make_init_request(self):
        pass

    def get_playlists(self):
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=self.cid,
                                                       client_secret=self.secret,
                                                       redirect_uri="http://127.0.0.1:8000/spotify/callback/",
                                                       scope="user-library-read"))
        test = sp.current_user()
        print(test['display_name'])

        results = sp.current_user_playlists()
        print(results['items'])

if __name__ == "__main__":
    test = PlaylistProcessor()
    test.get_playlists()
