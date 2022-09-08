import os
import DBProcessor
import spotipy
from dotenv import load_dotenv
from spotipy import SpotifyOAuth


class PlaylistProcessor:
    # used to check if the DB files exists and if it does, skip it. If it doesn't,
    # process it
    file_names = ['Top Billboard Hits 1950s', 'Top Billboard Hits 1960s',
                  'Top Billboard Hits 1970s', 'Top Billboard Hits 1980s',
                  'Top Billboard Hits 1990s', 'Top Billboard Hits 2000s',
                  'Top Billboard Hits 2010s', 'Top Billboard Hits 2020s']
    base_url = "https://api.spotify.com/v1/"
    profile_id = "3146an25jyfyfmtaj3hxgiuel73i"  # Tristan's Profile

    load_dotenv()
    cid = os.getenv("CID")
    secret = os.getenv("SECRET")
    credManager = SpotifyOAuth(client_id=cid, client_secret=secret, redirect_uri="http://localhost:8888/callback",
                               scope='user-library-read')
    sp = spotipy.Spotify(client_credentials_manager=credManager)

    def __init__(self):
        load_dotenv()

    def get_playlists(self):
        results = self.sp.current_user_playlists()
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
    def extract_song_information(self, uri_list, title_list):
        decade_dict = {}

        for x in range(len(uri_list)):
            temp_features = self.sp.audio_features(uri_list[x])
            decade_dict[uri_list[x]] = {"song_title": title_list[x],
                                        "bpm": temp_features[0]['tempo'],
                                        "danceability": temp_features[0]['danceability'],
                                        "loudness": temp_features[0]['loudness'],
                                        "speechiness": temp_features[0]['speechiness'],
                                        "acousticness": temp_features[0]['acousticness'],
                                        "duration_ms": temp_features[0]['duration_ms'], "key": temp_features[0]['key'],
                                        "instrumentalness": temp_features[0]['instrumentalness']}
        return decade_dict


if __name__ == "__main__":

    test = PlaylistProcessor()
    playlists = test.get_playlists()

    print("Looking for Playlists")
    for x in playlists['items']:
        print("----------------------")
        print(x['name'])
        print("----------------------")

        db_ops = DBProcessor.DBOps(x['name'])

        uris, titles = test.get_uris_and_titles(x['uri'])

        db_ops.initialize_db(x['name'])

        # This line does it ALL
        new_dict = test.extract_song_information(uris, titles)
        print(new_dict)
        db_ops.add_song_to_db(new_dict)
