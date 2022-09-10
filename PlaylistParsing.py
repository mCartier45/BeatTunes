import json
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
    def extract_song_information(self, uri_list, title_list, playlist_name):
        decade_dict = {}

        for x in range(len(uri_list)):
            temp_features = self.sp.audio_features(uri_list[x])
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
                                        "year": self.get_year(playlist_name)}
        return decade_dict

    def get_year(self, playlist_name):
        file = open("data/years.json")
        json_years = json.load(file)
        file.close()
        return json_years[0][playlist_name]


if __name__ == "__main__":

    test = PlaylistProcessor()
    playlists = test.get_playlists()
    db_ops = DBProcessor.DBOps()

    print("Looking for Playlists")
    if not os.path.exists("data/condensed.db"):

        for x in playlists['items']:
            playlist_name = x['name']
            print("----------------------")
            print(playlist_name)
            print("----------------------")

            uris, titles = test.get_uris_and_titles(x['uri'])

            db_ops.initialize_db()

            # This line does it ALL
            new_dict = test.extract_song_information(uris, titles, playlist_name)
            print(new_dict)
            db_ops.add_songs_to_db(new_dict)

    db_ops.print_all_bpms()

    print("Average BPM for year 1950: %d" % db_ops.get_avg_bpm(year="1980"))
    print(db_ops.debug_sql(query="select key from songs where year=1970"))
    print("The most common key in 2020 was: " + db_ops.get_most_common_key(year="1960"))
