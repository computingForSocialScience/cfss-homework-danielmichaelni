import pymysql
import json

dbname = 'facebook_networks'
host = 'localhost'
user = 'root'
passwd = ''
db = pymysql.connect(db=dbname, host=host, user=user, passwd=passwd, charset='utf8')

def create_sql_tables():
    cur = db.cursor()
    sql = '''CREATE TABLE IF NOT EXISTS friend_attributes (uid VARCHAR(255),
                                                           first_name VARCHAR(255),
                                                           middle_name VARCHAR(255),
                                                           last_name VARCHAR(255),
                                                           name VARCHAR(255),
                                                           pic VARCHAR(255),
                                                           religion VARCHAR(255),
                                                           birthday_date VARCHAR(255),
                                                           sex VARCHAR(255),
                                                           hometown_location VARCHAR(255),
                                                           current_location VARCHAR(255),
                                                           relationship_status VARCHAR(255),
                                                           significant_other_id VARCHAR(255),
                                                           political VARCHAR(255),
                                                           locale VARCHAR(255),
                                                           profile_url VARCHAR(255),
                                                           website VARCHAR(255));'''
    cur.execute(sql)
    sql = '''CREATE TABLE IF NOT EXISTS friend_edges (uid1 VARCHAR(255),
                                                      uid2 VARCHAR(255));'''
    cur.execute(sql)

    db.commit()

def input_sql_data():
    friend_attributes = process_friend_attributes()
    friend_edges = process_friend_edges()

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

def get_json(file_name):
    f = open(file_name)
    data = json.load(f)
    f.close()
    return data

def process_friend_attributes():
    friend_attributes = []
    friend_attributes_json = get_json('friend_attributes.json')
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
    return friend_attributes

def process_friend_edges():
    friend_edges = []
    friend_edges_json = get_json('friend_edges.json')
    for d in friend_edges_json:
        edges_tuple = (d['uid1'], d['uid2'])
        friend_edges.append(edges_tuple)
    return friend_edges