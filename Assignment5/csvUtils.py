from io import open

def writeArtistsTable(artist_info_list):
    """Given a list of dictionries, each as returned from 
    fetchArtistInfo(), write a csv file 'artists.csv'.

    The csv file should have a header line that looks like this:
    ARTIST_ID,ARTIST_NAME,ARTIST_FOLLOWERS,ARTIST_POPULARITY
    """
    f = open('artists.csv', 'w')
    f.write(u'ARTIST_ID,ARTIST_NAME,ARTIST_FOLLOWERS,ARTIST_POPULARITY\n')
    for artist_info in artist_info_list:
        artist_id = artist_info['id']
        artist_name = artist_info['name']
        artist_followers = unicode(artist_info['followers'])
        artist_popularity = unicode(artist_info['popularity'])
        f.write(artist_id + u',"' + artist_name + u'",' + artist_followers + u',' + artist_popularity + u'\n')
    f.close()
      
def writeAlbumsTable(album_info_list):
    """
    Given list of dictionaries, each as returned
    from the function fetchAlbumInfo(), write a csv file
    'albums.csv'.

    The csv file should have a header line that looks like this:
    ARTIST_ID,ALBUM_ID,ALBUM_NAME,ALBUM_YEAR,ALBUM_POPULARITY
    """
    f = open('albums.csv', 'w')
    f.write(u'ARTIST_ID,ALBUM_ID,ALBUM_NAME,ALBUM_YEAR,ALBUM_POPULARITY\n')
    for album_info in album_info_list:
        artist_id = album_info['artist_id']
        album_id = album_info['album_id']
        album_name = album_info['name']
        album_year = album_info['year']
        album_popularity = unicode(album_info['popularity'])
        f.write(artist_id + u',' + album_id + u',"' + album_name + u'",' + album_year + u',' + album_popularity + u'\n')
    f.close()