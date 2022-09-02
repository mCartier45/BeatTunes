import re
import requests
import os
import spotipy
from spotipy import *
from spotipy.oauth2 import SpotifyClientCredentials
from getURIs import getURIs

# create variables for spotify authentication
cid = 'a4d934e4e20c4eabba2aa6240c13cba4'
secret = 'd0815c59eb194a009b0cbeb6fb9a4e64'

# Create credential manager and spotify object
credManager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=credManager)

def createFeaturesJsons(uri, fileNum):
    results = sp.audio_features(uri)
    fileName = "FeatSong#" + str(fileNum)
    f = open("/Users/root1/Documents/pycharmProjects/pythonProject/FeatJsons/" + fileName + ".json", "x+")
    f.write(str(results))
    f.close()
def createAnalysisJsons(uri, fileNum):
    # Store audio_analysis in JSON file
    results = sp.audio_analysis(uri)
    fileName = "AnalSong#" + str(fileNum)
    f = open("/Users/root1/Documents/pycharmProjects/pythonProject/AnalJsons/" + fileName + ".json", "x+")
    f.write(str(results))
    f.close()


if __name__ == '__main__':

    # Create instance of getURIs
    inst = getURIs()
    url = "https://open.spotify.com/playlist/6PuUwX9HZfEs6xg9KjYYHR?si=529d0c6827ea447f"
    # Create array of URIs
    playlistUris = inst.getPlayListsURIs(url, sp)
    # playlistNames = inst.getTrackNames(url)
    # Loop through URIs and create JSONs
    j = 0
    for i in playlistUris:
        if j > 5:
            break
        createAnalysisJsons(i, j)
        createFeaturesJsons(i, j)
        j += 1
