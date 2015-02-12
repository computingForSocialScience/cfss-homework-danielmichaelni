import sys
from fetchArtist import fetchArtistId, fetchArtistInfo
from fetchAlbums import fetchAlbumIds, fetchAlbumInfo
from csvUtils import writeArtistsTable, writeAlbumsTable
from barChart import plotBarChart

if __name__ == '__main__':
    artist_names = sys.argv[1:]
    print "input artists are ", artist_names
    # YOUR CODE HERE
    artist_info_list = []
    album_info_list = []
    for name in artist_names:
        artist_id = fetchArtistId(name)
        artist_info = fetchArtistInfo(artist_id)
        artist_info_list.append(artist_info)

        album_ids = fetchAlbumIds(artist_id)
        for id in album_ids:
            album_info = fetchAlbumInfo(id)
            album_info_list.append(album_info)
    writeArtistsTable(artist_info_list)
    writeAlbumsTable(album_info_list)
    plotBarChart()