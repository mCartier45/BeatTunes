import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from getURIs import getURIs
from userLogin import GetUrls
import os

# create variables for spotify authentication
cid = 'a4d934e4e20c4eabba2aa6240c13cba4'
secret = 'd0815c59eb194a009b0cbeb6fb9a4e64'

# Create credential manager and spotify object
credManager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=credManager)

# Create objects
uriGetter = getURIs()
playlistGetter = GetUrls()

# set directory vars
parentDir = '/Users/root1/Documents/pycharmProjects/pythonProject/'

def createFeaturesJsons(uri, fileNum, path):
    results = sp.audio_features(uri)
    fileName = "FeatSong#" + str(fileNum)
    f = open(path + "/" + fileName + ".json", "x+")
    f.write(str(results))
    f.close()


if __name__ == '__main__':
    playlists = uriGetter.getPlaylistArray()
    names = uriGetter.getPlaylistNames()
    uris = []
    x = 1
    for i, playlist in enumerate(playlists):
        uris.append(uriGetter.getPlayListsURIs(playlist, sp))
        name = names[i]
        if os.path.isdir(os.path.join(parentDir, name)):
            name += str(x)
            path = os.path.join(parentDir, name)
            x += 1
        else:
            path = os.path.join(parentDir, name)
        #path = os.path.join(parentDir, name)
        os.makedirs(path)
        for j, uri in enumerate(uris):
            createFeaturesJsons(uri, j, path)
