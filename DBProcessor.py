import random
import sqlite3
import readJSON


class DBOps:
    connect = sqlite3.connect("beattunes.db")
    cursor = connect.cursor()

    def __init__(self):
        pass

    def add_song_to_db(self, song):
        keys = {0: "C", 1: "C#", 2: "D", 3: "D#", 4: "E",
                5: "F", 6: "F#", 7: "G", 8: "G#", 9: "A",
                10: "B Flat"}

        bpm = song.get("BPM")
        key = keys.get(song.get("key"))
        loudness = song.get("loudness")
        acoustic = song.get("acousticness")
        time_sig = song.get("Time Signature")
        dance = song.get("danceability")

        q = f"INSERT INTO songs VALUES ('{bpm}', '{key}','{loudness}','{acoustic}','{time_sig}','{dance}', null, null) "

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


if __name__ == "__main__":
    read_j = readJSON.ReadJSON()

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
