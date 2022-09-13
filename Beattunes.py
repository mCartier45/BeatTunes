import json
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

    file = open("data/years.json")
    years = json.load(file)

    for x in years[0]:
        print("The average BPM for " + str(years[0][x]) + " is: %d" % db_ops.get_avg_bpm(year=years[0][x]))

    print("The most common key in 2020 was: " + db_ops.get_most_common_key(year="2020"))

    db_ops.close_db()
