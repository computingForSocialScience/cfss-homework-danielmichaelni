from flask import Flask, render_template, request, redirect, url_for
import pymysql

from artistNetworks import *
from analyzeNetworks import *
from makePlaylist import *

dbname="playlists"
host="localhost"
user="root"
passwd=""
db=pymysql.connect(db=dbname, host=host, user=user,passwd=passwd, charset='utf8')

app = Flask(__name__)


@app.route('/')
def make_index_resp():
    # this function just renders templates/index.html when
    # someone goes to http://127.0.0.1:5000/
    return(render_template('index.html'))


@app.route('/playlists/')
def make_playlists_resp():
    cur = db.cursor()
    cur.execute('SELECT * FROM playlists;')
    playlists = cur.fetchall()
    print playlists
    return render_template('playlists.html',playlists=playlists)


@app.route('/playlist/<playlistId>')
def make_playlist_resp(playlistId):
    return render_template('playlist.html',songs=songs)


@app.route('/addPlaylist/',methods=['GET','POST'])
def add_playlist():
    if request.method == 'GET':
        # This code executes when someone visits the page.
        return(render_template('addPlaylist.html'))
    elif request.method == 'POST':
        # this code executes when someone fills out the form
        artistName = request.form['artistName']
        # YOUR CODE HERE
        return(redirect("/playlists/"))


def createNewPlaylist(name):
    cur = db.cursor()
    sql = '''CREATE TABLE IF NOT EXISTS playlists (id INTEGER PRIMARY KEY AUTO_INCREMENT,
                                                   rootArtist VARCHAR(255));'''
    cur.execute(sql)
    sql = '''CREATE TABLE IF NOT EXISTS songs (playlistId INTEGER,
                                               songOrder INTEGER,
                                               artistName VARCHAR(255),
                                               albumName VARCHAR(255),
                                               trackName VARCHAR(255));'''
    cur.execute(sql)
    
    cur.execute('INSERT INTO playlists (rootArtist) VALUES (%s);', name)
    playlist_id = cur.lastrowid

    edgeList = getEdgeList(fetchArtistId(name), 2)
    dg = pandasToNetworkX(edgeList)
    sample = []
    for i in range(30):
        sample.append(randomCentralNode(dg))

    songs_list = []
    i = 0
    for a in sample:
        artist_name = fetchArtistInfo(a)['name']
        try:
            album_id = random.choice(fetchAlbumIds(a))
        except:
            print 'artist %s has no albums' % artist_name
            continue
        album_name = fetchAlbumInfo(album_id)['name']
        track_name = random.choice(fetchTrackNames(album_id))
        songs_list.append((playlist_id, i, artist_name, album_name, track_name))
        i += 1

    insert_query = '''INSERT INTO songs (playlistId, songOrder, artistName, albumName, trackName) VALUES (%s, %s, %s, %s, %s);'''
    print songs_list
    cur.executemany(insert_query, songs_list)

    db.commit()

if __name__ == '__main__':
    app.debug=True
    app.run()