import sys
import random

from artistNetworks import *
from analyzeNetworks import *

SPOTIFY_API_BASE_URL = 'https://api.spotify.com'

def fetchArtistId(name):
    url = SPOTIFY_API_BASE_URL + '/v1/search/?q=' + name + '&type=artist'
    req = requests.get(url)
    data = req.json()
    return data['artists']['items'][0]['id']

def fetchAlbumIds(artist_id):
    url = SPOTIFY_API_BASE_URL + '/v1/artists/' + artist_id + '/albums?market=US&album_type=album'
    req = requests.get(url)
    data = req.json()
    albumIds = []
    for album in data['items']:
        albumIds.append(album['id'])
    return albumIds

def fetchArtistInfo(artist_id):
    url = SPOTIFY_API_BASE_URL + '/v1/artists/' + artist_id
    req = requests.get(url)
    data = req.json()
    artist_info = {}
    artist_info['followers'] = data['followers']['total']
    artist_info['genres'] = data['genres']
    artist_info['id'] = data['id']
    artist_info['name'] = data['name']
    artist_info['popularity'] = data['popularity']
    return artist_info

def fetchAlbumInfo(album_id):
    url = SPOTIFY_API_BASE_URL + '/v1/albums/' + album_id
    req = requests.get(url)
    data = req.json()
    album_info = {}
    album_info['artist_id'] = data['artists'][0]['id']
    album_info['album_id'] = data['id']
    album_info['name'] = data['name']
    album_info['year'] = data['release_date'][:4]
    album_info['popularity'] = data['popularity']
    return album_info

def fetchTrackNames(album_id):
    url = SPOTIFY_API_BASE_URL + '/v1/albums/' + album_id + '/tracks'
    req = requests.get(url)
    data = req.json()
    trackNames = []
    for track in data['items']:
        trackNames.append(track['name'])
    return trackNames

if __name__ == '__main__':
    artists = [fetchArtistId(name) for name in sys.argv[1:]]
    
    edgeList = getEdgeList(artists.pop(), 2)
    for a in artists:
        edgeList = combinegeEdgeLists(edgeList, getEdgeList(a, 2))
    
    dg = pandasToNetworkX(edgeList)
    
    sample = []
    for i in range(30):
        sample.append(randomCentralNode(dg))
    
    playlist = []
    for a in sample:
        artist_name = fetchArtistInfo(a)['name']
        album_id = random.choice(fetchAlbumIds(a))
        album_name = fetchAlbumInfo(album_id)['name']
        track_name = random.choice(fetchTrackNames(album_id))
        playlist.append((artist_name, album_name, track_name))

    pd.DataFrame(playlist, columns=['artist_name', 'album_name', 'track_name']).to_csv('playlist.csv', index=False, encoding='utf-8')