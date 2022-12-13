import json
import os
import random
import sqlite3
import string

import PlaylistParsing


class DBOps:

    def __init__(self, db_name):
        self.db_path = "data/" + db_name + ".db"
        if os.path.exists(self.db_path):
            self.connect = sqlite3.connect(self.db_path)
            self.cursor = self.connect.cursor()
        else:
            self.cursor = None
            self.connect = None

    def initialize_db(self):
        # Line creates the DB
        self.connect = sqlite3.connect(self.db_path)
        self.cursor = self.connect.cursor()
        # SQL to create the table if it doesn't exist.
        self.cursor.execute('''
          CREATE TABLE IF NOT EXISTS songs
          (title TEXT, 
           key TEXT,
           tempo INTEGER,
           danceability INTEGER,
           loudness INTEGER,
           acousticness INTEGER,
           duration_ms INTEGER,
           year INTEGER,
           uri TEXT,
           playlist TEXT,
           id TEXT primary key,
           energy TEXT,
           liveness TEXT,
           time_signature TEXT,
           valence TEXT,
           instrumentallness TEXT,
           mode TEXT)
          ''')
        # Commit DB Chances
        self.connect.commit()

        # Init Playlist Processing
        print("Looking for Playlists")
        process_playlist = PlaylistParsing.PlaylistProcessor()
        playlists = process_playlist.get_playlists()
        additional_playlists = process_playlist.get_playlists(offset=50)

        # Add songs from playlists to database
        for x in playlists['items']:
            playlist_name = x['name']
            print("----------------------")
            print(playlist_name)
            print("----------------------")

            uris, titles = process_playlist.get_uris_and_titles(x['uri'])

            # Problem Line
            new_dict = process_playlist.extract_song_information(uris, titles, playlist_name)
            print(new_dict)
            self.add_songs_to_db(new_dict)

        for x in additional_playlists['items']:
            playlist_name = x['name']
            print("----------------------")
            print(playlist_name)
            print("----------------------")

            uris, titles = process_playlist.get_uris_and_titles(x['uri'])

            # Problem Line
            new_dict = process_playlist.extract_song_information(uris, titles, playlist_name)
            print(new_dict)
            self.add_songs_to_db(new_dict)

    def add_songs_to_db(self, song_dict):

        # Open keys JSON file for below processing
        file = open("data/keys.json")
        keys = json.load(file)
        file.close()

        # Get all song attributes and add them to the dictionary.
        for song in song_dict:
            bpm = song_dict[song].get("bpm")
            key = keys[0][(str(song_dict[song].get("key")))]
            loudness = song_dict[song].get("loudness")
            acoustic = song_dict[song].get("acousticness")
            dance = song_dict[song].get("danceability")
            title = song_dict[song].get("title")
            duration_ms = song_dict[song].get("duration_ms")
            uri = song_dict[song].get("uri")
            year = song_dict[song].get("year")
            energy = song_dict[song].get("energy")
            liveness = song_dict[song].get("liveness")
            time_signature = song_dict[song].get("time_signature")
            valence = song_dict[song].get("valence")
            instrumentalness = song_dict[song].get("instrumentalness")
            mode = self.convert_mode(int(song_dict[song].get("mode")))
            id = ''.join(random.choices(string.ascii_uppercase +
                                        string.digits, k=25))
            playlist = song_dict[song].get("playlist")

            print(playlist, title, bpm, key, loudness, acoustic, dance, duration_ms, energy, liveness, time_signature, valence, instrumentalness, mode, uri)

            # Switch away from this to disallow sql injection
            q = "INSERT INTO songs VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

            self.cursor.execute(q, [title, key, bpm, dance, loudness, acoustic, duration_ms, year, uri, playlist, id, energy, liveness, time_signature, valence, instrumentalness, mode])
            self.connect.commit()

    def print_all_bpms(self):
        # SQL returns title + tempo, only used for printing, void method
        for x in self.cursor.execute("select tempo, title from songs"):
            print("-------------------------------")
            print("TITLE: ", x[1])
            print("BPM: ", x[0])
            print("-------------------------------")

    def print_all_uris(self):
        for x in self.cursor.execute("select uri from songs"):
            print(x[0])

    def get_avg_bpm(self, year):
        for x in self.cursor.execute("select avg(tempo) from songs where year=" + str(year)):
            return x[0]

    def get_most_common_key(self, year):
        # Returns most common key via SQL
        q = "SELECT key FROM songs WHERE year=" + year + " GROUP BY key ORDER BY key DESC LIMIT 1"
        for x in self.cursor.execute(q):
            return x[0]

    def convert_mode(self, mode):
        if mode == 0:
            return "minor"
        else:
            return "major"

    def close_db(self):
        self.cursor.close()
        self.connect.close()
