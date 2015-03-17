from flask import Flask, render_template
import pymysql
import json

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
    friends = cur.fetchall()

    return render_template('index.html', friends=friends)

def initialize_db():
    create_sql_tables()
    input_sql_data()

if __name__ == '__main__':
    initialize_db()
    app.debug = True
    app.run()