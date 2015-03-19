from flask import Flask, request, render_template, redirect
import pymysql
import json
import networkx as nx
import matplotlib.pyplot as plt
import tempfile

from initialization import *

dbname = 'facebook_networks'
host = 'localhost'
user = 'root'
passwd = ''
db = pymysql.connect(db=dbname, host=host, user=user, passwd=passwd, charset='utf8')

app = Flask(__name__)

@app.route('/')
def index():
    cur = db.cursor()
    cur.execute('SELECT uid, name FROM friend_attributes;')
    friends = cur.fetchall()[:100]

    return render_template('index.html', friends=friends)

@app.route('/profile/<userid>')
def profile(userid):
    cur = db.cursor()
    cur.execute('SELECT name, pic, sex, birthday_date, profile_url, current_location FROM friend_attributes WHERE uid = %s;', userid)
    attrs = cur.fetchall()
    print attrs
    attrs = attrs[0]
    name, pic, sex, birthday, profile_url, current_location = attrs[0], attrs[1], attrs[2], attrs[3], attrs[4], attrs[5]
    
    loc = 'N/A'
    if current_location != 'null':
        loc_dict = json.loads(current_location)
        loc = loc_dict['city'] + ', ' + loc_dict['country']

    cur.execute('SELECT uid1, uid2 FROM friend_edges WHERE uid1 = %s;', name)
    friends = cur.fetchall()[:100]

    G = nx.Graph()
    G.clear()
    G.add_edges_from(friends)

    friends_with_id = []
    for f in friends:
        cur.execute('SELECT uid FROM friend_attributes WHERE name = %s LIMIT 1;', f[1])
        uid = cur.fetchall()
        if uid != ():
            friends_with_id.append((uid[0][0], f[1]))

    plt.clf()
    nx.draw(G, node_color='b', alpha=0.6)
    f = tempfile.NamedTemporaryFile(dir='static/temp',
                                    suffix='.png',
                                    delete=False)
    plt.savefig(f)
    f.close()
    graph_url = f.name.split('/')[-1]

    return render_template('profile.html', name=name,
                                           pic=pic,
                                           sex=sex,
                                           birthday=birthday,
                                           profile_url=profile_url,
                                           loc = loc,
                                           friends_with_id=friends_with_id,
                                           graph_url=graph_url)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        friend_attributes_json = json.loads(request.form['friend_attributes'])
        friend_edges_json = json.loads(request.form['friend_edges'])

        friend_attributes = []
        for d in friend_attributes_json:
            attributes_tuple = (d['uid'],
                                d['first_name'],
                                d['middle_name'],
                                d['last_name'],
                                d['name'],
                                d['pic'],
                                d['religion'],
                                d['birthday_date'],
                                d['sex'],
                                json.dumps(d['hometown_location']),
                                json.dumps(d['current_location']),
                                d['relationship_status'],
                                d['significant_other_id'],
                                d['political'],
                                d['locale'],
                                d['profile_url'],
                                d['website'])
            friend_attributes.append(attributes_tuple)
        
        friend_edges = []
        for d in friend_edges_json:
            edges_tuple = (d['uid1'], d['uid2'])
            friend_edges.append(edges_tuple)

        drop_sql_tables()
        create_sql_tables()

        cur = db.cursor()
        sql = '''INSERT INTO friend_attributes
                 (uid, first_name, middle_name, last_name, name, pic, religion,
                  birthday_date, sex, hometown_location, current_location,
                  relationship_status, significant_other_id, political, locale,
                  profile_url, website)
                 VALUES
                 (%s, %s, %s, %s, %s, %s, %s, %s, %s,
                  %s, %s, %s, %s, %s, %s, %s, %s);'''
        cur.executemany(sql, friend_attributes)
        sql = '''INSERT INTO friend_edges (uid1, uid2) VALUES (%s, %s);'''
        cur.executemany(sql, friend_edges)

        db.commit()

        return redirect('/')
    else:
        return render_template('upload.html')

def initialize_db():
    drop_sql_tables()
    create_sql_tables()
    input_sql_data()

if __name__ == '__main__':
    initialize_db()
    app.debug = True
    app.run()