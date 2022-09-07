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

    # TODO: Use this method to return a dictionary of relevant information
    # and save it to the database.
    def extract_song_information(self, title_list, uri_list):
        for x in range(len(uri_list)):
            temp = self.sp.audio_features(uri_list[x])
            print("-------------------------")
            print("Song Title: ", title_list[x])
            print("BPM: ", temp[0]['tempo'])
            print("Danceability: ", temp[0]['danceability'])

if __name__ == "__main__":

    test = PlaylistProcessor()
    playlists = test.get_playlists()

    print("Looking for Playlists")

    for x in playlists['items']:
        print("----------------------")
        print(x['name'])
        print("----------------------")

        # This line does it ALL
        test.extract_song_information(test.get_titles(playlist_uri=x['uri']), test.get_uris(playlist_uri=x['uri']))

