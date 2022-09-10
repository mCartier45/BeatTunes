import os
import DBProcessor
from PlaylistParsing import PlaylistProcessor

if __name__ == "__main__":

    process_playlist = PlaylistProcessor()
    playlists = process_playlist.get_playlists()

    db_ops = DBProcessor.DBOps()

    print("Looking for Playlists")

    if not os.path.exists(db_ops.db_path):
        db_ops.initialize_db()

    db_ops.print_all_bpms()

    year = ["1950", "1960", "1970", "1980", "1990", "2000", "2010", "2020"]
    for x in range(len(year)):
        print("The average BPM for " + year[x] + " is: %d" % db_ops.get_avg_bpm(year=year[x]))

    print("The most common key in 2020 was: " + db_ops.get_most_common_key(year="1960"))

    db_ops.close_db()
