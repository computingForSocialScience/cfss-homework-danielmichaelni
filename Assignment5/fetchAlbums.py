import requests
from datetime import datetime

SPOTIFY_API_BASE_URL = 'https://api.spotify.com'

def fetchAlbumIds(artist_id):
    """Using the Spotify API, take an artist ID and 
    returns a list of album IDs in a list
    """
    url = SPOTIFY_API_BASE_URL + '/v1/artists/' + id + '/albums?market=US&album_type=album'
    req = requests.get(url)
    data = req.json()
    albumIds = []
    for album in data['items']:
        albumIds.append(album['id'])
    return albumIds

def fetchAlbumInfo(album_id):
    """Using the Spotify API, take an album ID 
    and return a dictionary with keys 'artist_id', 'album_id' 'name', 'year', popularity'
    """
    url = SPOTIFY_API_BASE_URL + '/v1/albums/' + id
    req = requests.get(url)
    data = req.json()
    return data