import os
import webbrowser
from urllib.parse import urlencode

import requests
import spotipy
from dotenv import load_dotenv
from spotipy import SpotifyClientCredentials, SpotifyOAuth


class PlaylistProcessor:
    # api_endpoint = https://api.spotify.com/v1/users/user_id/playlists
    base_url = "https://api.spotify.com/v1/"
    profile_id = "3146an25jyfyfmtaj3hxgiuel73i"  # Tristan's Profile

    load_dotenv()
    cid = os.getenv("CID")
    secret = os.getenv("SECRET")
    credManager = SpotifyOAuth(client_id=cid, client_secret=secret, redirect_uri="http://localhost:8888/callback", scope='user-library-read')
    sp = spotipy.Spotify(client_credentials_manager=credManager)

    def __init__(self):
        load_dotenv()
        self.make_init_request()

    def get_playlist_request(self):
        pass

    def make_init_request(self):
        pass

    def get_playlists(self):
        results = self.sp.current_user_playlists()
        for x in results['items']:
            print(x['name'])

        if len(results) == 0:
            print("No playlists Found")
        return results

    def parse_playlist(self, playlist_uri):
        tracks = self.sp.playlist_items(playlist_id=playlist_uri)
        for x in tracks['items']:
            print(x['track']['name'])


if __name__ == "__main__":
    test = PlaylistProcessor()
    playlists = test.get_playlists()

    print("Looking for Playlists")

    print(playlists)

    for x in playlists['items']:
        print("----------------------")
        print(x['name'])
        print("----------------------")
        test.parse_playlist(playlist_uri=x['uri'])
