import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

class getURIs:
    """
    cid = 'a4d934e4e20c4eabba2aa6240c13cba4'
    secret = 'd0815c59eb194a009b0cbeb6fb9a4e64'
    credManager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
    sp = spotipy.Spotify(client_credentials_manager=credManager)
    """

    def __init__(self):
        pass

    def getTrackNames(self, playlistID, sp):
        results = sp.playlist_tracks(playlistID)
        playlist_items = results['items']
        ids = []

        while results['next']:
            results = sp.next(results)
            playlist_items.append(results['items'])

        for item in playlist_items:
            track_id = item["track"]["id"]
            ids.append(track_id)
        return ids

    def getPlayListsURIs(self, playlistID, sp):
        results = sp.playlist_tracks(playlistID)
        playlist_items = results['items']
        uris = []

        while results['next']:
            results = sp.next(results)
            playlist_items.append(results['items'])

        for item in playlist_items:
            track_uri = item["track"]["uri"]
            uris.append(track_uri)
        return uris
