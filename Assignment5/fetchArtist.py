import sys
import requests
import csv

SPOTIFY_API_BASE_URL = 'https://api.spotify.com'

def fetchArtistId(name):
    """Using the Spotify API search method, take a string that is the artist's name, 
    and return a Spotify artist ID.
    """
    url = SPOTIFY_API_BASE_URL + '/v1/search/?q=' + name + '&type=artist'
    req = requests.get(url)
    data = req.json()
    return data['artists']['items'][0]['id']

def fetchArtistInfo(artist_id):
    """Using the Spotify API, takes a string representing the id and
`   returns a dictionary including the keys 'followers', 'genres', 
    'id', 'name', and 'popularity'.
    """
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