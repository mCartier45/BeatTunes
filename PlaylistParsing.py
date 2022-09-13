import json
import os
import DBProcessor
import spotipy
from dotenv import load_dotenv
from spotipy import SpotifyOAuth

'''
Method: Playlist Processor
Use: Access user's profile and parse their playlists. Integrated with DBProcessor file.
'''


class PlaylistProcessor:
    def __init__(self):
        load_dotenv()
        self.cid = os.getenv("CID")
        self.secret = os.getenv("SECRET")
        self.credManager = SpotifyOAuth(client_id=self.cid, client_secret=self.secret,
                                        redirect_uri="http://localhost:8888/callback",
                                        scope='user-library-read')
        self.sp = spotipy.Spotify(client_credentials_manager=self.credManager)

    def get_playlists(self, offset=0):
        results = self.sp.current_user_playlists(limit=50, offset=offset)
        for x in results['items']:
            print(x['name'])

        if len(results) == 0:
            print("No playlists Found")
        return results

    def get_uris_and_titles(self, playlist_uri):
        tracks = self.sp.playlist_items(playlist_id=playlist_uri)
        track_uris = []
        track_names = []

        for x in tracks['items']:
            track_uris.append(x['track']['uri'])
            track_names.append(x['track']['name'])
        return track_uris, track_names

    # TODO: Use this method to return a dictionary of relevant information
    # and save it to the database.
    def extract_song_information(self, uri_list, title_list, playlist_name):
        decade_dict = {}

        for x in range(len(uri_list)):
            temp_features = self.sp.audio_features(uri_list[x])
            temp_artist = self.sp.track(uri_list[x])
            print("TEST ARTIST:", temp_artist)
            print("RELEASE YEAR: " + temp_artist['album']['release_date'][0:4])
            print("\n\n\n")
            # Creates an entry in the dictionary to return
            try:
                decade_dict[uri_list[x]] = {"song_title": title_list[x],
                                            "bpm": temp_features[0]['tempo'],
                                            "danceability": temp_features[0]['danceability'],
                                            "loudness": temp_features[0]['loudness'],
                                            "speechiness": temp_features[0]['speechiness'],
                                            "acousticness": temp_features[0]['acousticness'],
                                            "duration_ms": temp_features[0]['duration_ms'],
                                            "key": temp_features[0]['key'],
                                            "instrumentalness": temp_features[0]['instrumentalness'],
                                            "title": title_list[x],
                                            "uri": uri_list[x],
                                            "year": temp_artist['album']['release_date'][0:4]}
            except:
                continue
        return decade_dict