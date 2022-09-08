import os
import sqlite3



class DBOps:

    def __init__(self, db):
        self.connect = sqlite3.connect("data/" + db + ".db")
        self.cursor = self.connect.cursor()


    def initialize_db(self, playlist):
        # file = open("data/" + playlist + ".db", "x")
        self.cursor.execute('''
          CREATE TABLE IF NOT EXISTS songs
          (title TEXT primary key, 
           key TEXT,
           tempo INTEGER,
           danceability INTEGER,
           loudness INTEGER,
           acousticness INTEGER,
           duration_ms INTEGER)
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
            speech = song_dict[song].get("speechiness")

            print(bpm, key, loudness, acoustic, dance, title, duration_ms)

            # Need to place these into the order that the values are inserted
            q = f"INSERT INTO songs VALUES ('{title}', '{key}','{bpm}','{dance}','{loudness}', '{acoustic}', '{duration_ms}')"

            self.cursor.execute(q)
            self.connect.commit()

    def print_db(self):

        for x in self.cursor.execute("select BPM from songs"):
            print(x[0])

    def get_avg_bpm(self):
        total = 0
        average = 0
        result = 0
        for x in self.cursor.execute("select BPM from songs"):
            result += float(x[0])
            total += 1

        average = result / total # Basic Avg calculation
        print("The average BPM for the Billboard Top 100 in 1972 is: %.3f" % average)

        return average

    def get_most_common_key(self):
        most_common = "Default Key"
        list_of_keys = []
        counter = 0

        for x in self.cursor.execute("select key from songs"): # Append to List
            list_of_keys.append(x[0])

        for x in list_of_keys: # Loop list and find most common
            current_frequency = list_of_keys.count(x)

            if current_frequency > counter:
                counter = current_frequency
                most_common = x

        print(most_common)
        return most_common

    def close_db(self):
        self.cursor.close()
        self.connect.close()

    def check_if_db_exists(self, db_name):
        if os.path.exists("data/" + db_name + ".db"):
            return True
        else:
            return False

if __name__ == "__main__":

    # read_j.replace_single_quotes(file="FeatSong0.json")
    # test_song = read_j.parse_json(file="FeatSong0.json")

    db_ops = DBOps()
    for i in range(100):
        pass
        # db_ops.add_song_to_db(test_song)

    db_ops.print_db()
    db_ops.get_avg_bpm()
    db_ops.get_most_common_key()





    db_ops.close_db()
