import json
import os
import DBProcessor
from PlaylistParsing import PlaylistProcessor

if __name__ == "__main__":

    #  get user information and initialize the database
    process_playlist = PlaylistProcessor()
    user = process_playlist.user_info['display_name']
    db_ops = DBProcessor.DBOps(user)

    print("Looking for Playlists")
    if not os.path.exists(db_ops.db_path):
        db_ops.initialize_db()



    db_ops.print_all_bpms()

    playlists = process_playlist.get_playlists()
    print(playlists)

    db_ops.print_all_bpms()

    db_ops.close_db()
