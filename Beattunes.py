import json
import os
import DBProcessor
from PlaylistParsing import PlaylistProcessor

if __name__ == "__main__":

    # TODO: Check if offset index starts at 0 or 1
    process_playlist = PlaylistProcessor()

    db_ops = DBProcessor.DBOps()

    print("Looking for Playlists")
    if not os.path.exists(db_ops.db_path):
        db_ops.initialize_db()

    db_ops.print_all_bpms()

    file = open("data/years.json")
    year = json.load(file)

    for x in year[0]:
        print(year[0][x])

    # for x in year[0]:
    # print("The average BPM for " + str(year[0][x]) + " is: %d" % db_ops.get_avg_bpm(year=year[0][x]))

    playlists = process_playlist.get_playlists()
    print(playlists)

    print("The most common key in 2020 was: " + db_ops.get_most_common_key(year="2020"))

    db_ops.close_db()
