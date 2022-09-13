import urllib.request
from pathlib import Path

import requests


class DownloadDB:
    def __init__(self):
        self.download_database()

    def download_database(self):
        url = "https://dl.dropboxusercontent.com/s/92egrpkkf7ar044/beattunes.db?dl=0"
        r = requests.get(url)
        print(len(r.content))
        filename = Path("data/beattunes.db")
        filename.write_bytes(r.content)


if __name__ == "__main__":
    dl_db = DownloadDB()