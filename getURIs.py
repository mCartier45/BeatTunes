import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from userLogin import GetUrls

class getURIs:

    def __init__(self):
        pass

    def getPlaylistArray(self):
        user = GetUrls()
        playlists = user.getUrls()
        return playlists

    def getPlaylistNames(self):
        user = GetUrls()
        names = user.getPlaylistNames()
        return names

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

