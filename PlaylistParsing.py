import math
import os

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
        self.user_info = self.sp.current_user()

    def get_playlists(self, offset=0):
        results = self.sp.current_user_playlists(offset=offset)
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

    def merge(self, dict1, dict2):
        toReturn = dict1 | dict2
        return toReturn

    def extract_song_information(self, uri_list, title_list, playlist_name):
        decade_dict = {}

        temp_features = self.sp.audio_features(uri_list)

        size_of_artist_lists = math.floor(len(uri_list) / 2)

        temp_artists = self.sp.tracks(uri_list[0:size_of_artist_lists])
        print("Temp Artist Length: ", len(temp_artists['tracks']))
        temp_artist_extra = self.sp.tracks(uri_list[size_of_artist_lists:len(uri_list)])
        print("Temp Artist Extra Length: ", len(temp_artist_extra['tracks']))
        dict_artists = self.merge(temp_artists, temp_artist_extra)
        print("LENGTH OF TEMP ARTIST (SHOULD BE 40 OR 100): ", len(dict_artists))
        n = 0

        for x in range(len(uri_list)):
            print("N: ", n)
            # print("TITLE:", title_list[x])
            # print("RELEASE YEAR: ", dict_artists['tracks'][x]['album']['release_date'])
            # print("\n\n\n")
            # Creates an entry in the dictionary to return
            try:
                decade_dict[uri_list[x]] = {"song_title": title_list[x],
                                            "bpm": temp_features[x]['tempo'],
                                            "danceability": temp_features[x]['danceability'],
                                            "loudness": temp_features[x]['loudness'],
                                            "speechiness": temp_features[x]['speechiness'],
                                            "acousticness": temp_features[x]['acousticness'],
                                            "duration_ms": temp_features[x]['duration_ms'],
                                            "key": temp_features[x]['key'],
                                            "energy": temp_features[x]['energy'],
                                            "liveness": temp_features[x]['liveness'],
                                            "mode": temp_features[x]['mode'],
                                            "time_signature": temp_features[x]['time_signature'],
                                            "valence": temp_features[x]['valence'],
                                            "instrumentalness": temp_features[x]['instrumentalness'],
                                            "title": title_list[x],
                                            "uri": uri_list[x],
                                            "year": playlist_name[18:22],
                                            "playlist": playlist_name}
                n += 1

            except:
                print("Song is null")

        print(decade_dict)

        return decade_dict
