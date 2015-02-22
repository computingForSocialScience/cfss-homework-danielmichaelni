import requests
import pandas as pd

SPOTIFY_API_BASE_URL = 'https://api.spotify.com'

def getRelatedArtists(artistID):
    url = SPOTIFY_API_BASE_URL + '/v1/artists/' + artistID + '/related-artists'
    req = requests.get(url)
    data = req.json()
    relatedArtists = []
    for artist in data['artists']:
        relatedArtists.append(artist['id'])
    return relatedArtists

def getDepthEdges(artistID, depth):
    if depth < 1:
        return []

    relatedArtists = getRelatedArtists(artistID)    
    depthEdges = [(artistID, related) for related in relatedArtists]

    if depth == 1:
        return depthEdges
    for aID in relatedArtists:
        depthEdges += getDepthEdges(aID, depth - 1)
    return list(set(depthEdges))

def getEdgeList(artistID, depth):
    return pd.DataFrame(getDepthEdges(artistID, depth), columns=['artist1', 'artist2'])

def writeEdgeList(artistID, depth, filename):
    getEdgeList(artistID, depth).to_csv(filename, index=False, encoding='utf-8')