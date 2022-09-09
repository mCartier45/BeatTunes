import os
import sqlite3


class DBOps:

    def __init__(self):
        if os.path.exists("data/condensed.db"):
            self.connect = sqlite3.connect("data/condensed.db")
            self.cursor = self.connect.cursor()
        else:
            self.cursor = None
            self.connect = None

    def initialize_db(self):
        self.connect = sqlite3.connect("data/condensed.db")
        self.cursor = self.connect.cursor()
        # file = open("data/" + playlist + ".db", "x")
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
           uri TEXT primary key)
          ''')
        self.connect.commit()

    def add_songs_to_db(self, song_dict):
        keys = {0: "C", 1: "C#", 2: "D", 3: "D#", 4: "E",
                5: "F", 6: "F#", 7: "G", 8: "G#", 9: "A",
                10: "B Flat", 11: "B"}
        for song in song_dict:
            bpm = song_dict[song].get("bpm")
            key = keys.get(song_dict[song].get("key"))
            loudness = song_dict[song].get("loudness")
            acoustic = song_dict[song].get("acousticness")
            dance = song_dict[song].get("danceability")
            title = song_dict[song].get("title")
            duration_ms = song_dict[song].get("duration_ms")
            uri = song_dict[song].get("uri")
            year = song_dict[song].get("year")

            print(bpm, key, loudness, acoustic, dance, title, duration_ms, uri)

            # Switch away from this to disallow sql injection
            q = "INSERT INTO songs VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"

            self.cursor.execute(q, [title, key, bpm, dance, loudness, acoustic, duration_ms, year, uri])
            self.connect.commit()

    def print_all_bpms(self):
        for x in self.cursor.execute("select tempo, title from songs"):
            print("-------------------------------")
            print("TITLE: ", x[1])
            print("BPM: ", x[0])
            print("-------------------------------")

    def print_all_uris(self):
        for x in self.cursor.execute("select uri from songs"):
            print(x[0])

    def get_avg_bpm(self, year):
        for x in self.cursor.execute("select avg(tempo) from songs where year=" + year):
            print(x[0])
            return x[0]

    def debug_sql(self, query):
        for x in self.cursor.execute(query):
            print(x[0])

    def get_most_common_key(self, year):
        q = "SELECT key FROM songs WHERE year=" + year + " GROUP BY key ORDER BY key DESC LIMIT 1"
        for x in self.cursor.execute(q):
            print(x[0])
            return x[0]

    def close_db(self):
        self.cursor.close()
        self.connect.close()

    def check_if_db_exists(self, db_name):
        if os.path.exists("data/" + db_name + ".db"):
            return True
        else:
            return False
