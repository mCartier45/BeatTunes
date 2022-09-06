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
        # TODO: Clean this up a bit because goddamn
    def get_uris(self, playlist_uri):
        tracks = self.sp.playlist_items(playlist_id=playlist_uri)
        track_uris = []

        for x in tracks['items']:
            track_uris.append(x['track']['uri'])
        return track_uris

    def get_titles(self, playlist_uri):
        tracks = self.sp.playlist_items(playlist_id=playlist_uri)
        track_names = []
        for x in tracks['items']:
            track_names.append(x['track']['name'])
        return track_names

    def extract_song_information(self, track_list):
        # for x in track_list:
        # TODO: Make this do everything, including getting titles and getting URI's and then displaying the results.
        temp = self.sp.audio_features(track_list[0])
        print("BPM: ", temp[0]['tempo'])
        print("Danceability: ", temp[0]['danceability'])

if __name__ == "__main__":
    test = PlaylistProcessor()
    playlists = test.get_playlists()

    print("Looking for Playlists")

    print(playlists)

    for x in playlists['items']:
        print("----------------------")
        print(x['name'])
        print("----------------------")

        print(test.get_titles(playlist_uri=x['uri'])[0])
        test.extract_song_information(test.get_uris(playlist_uri=x['uri']))
        print(test.get_titles(playlist_uri=x['uri'])[0])

