import json
import os
import random
import sqlite3
import string

import PlaylistParsing


class DBOps:

    def __init__(self):
        self.db_path = "data/beattunes.db"
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
           id TEXT primary key)
          ''')
        # Commit DB Chances
        self.connect.commit()

        # Init Playlist Processing
        process_playlist = PlaylistParsing.PlaylistProcessor()
        playlists = process_playlist.get_playlists()

        print("Looking for Playlists")
        # Add songs from playlists to database
        for x in playlists['items']:
            playlist_name = x['name']
            print("----------------------")
            print(playlist_name)
            print("----------------------")

            uris, titles = process_playlist.get_uris_and_titles(x['uri'])

            # This line does it ALL
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
            id = ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k=25))

            print(bpm, key, loudness, acoustic, dance, title, duration_ms, uri)

            # Switch away from this to disallow sql injection
            q = "INSERT INTO songs VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

            self.cursor.execute(q, [title, key, bpm, dance, loudness, acoustic, duration_ms, year, uri, id])
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

    def debug_sql(self, query):
        for x in self.cursor.execute(query):
            print(x[0])

    def get_most_common_key(self, year):
        # Returns most common key via SQL
        q = "SELECT key FROM songs WHERE year=" + year + " GROUP BY key ORDER BY key DESC LIMIT 1"
        for x in self.cursor.execute(q):
            return x[0]

    def close_db(self):
        self.cursor.close()
        self.connect.close()
