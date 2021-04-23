import sqlite3
from sqlite3 import Error

DB_FILE = 'testi.db'

def connect_database(database_file):
    connection = None

    try:
        connection = sqlite3.connect(database_file)
    except Error as e:
        print(e)

    return connection

def select_all(connection):

    cursor = connection.cursor()

    cursor.execute("select * from url")

    rows = cursor.fetchall()

    for row in rows:
        print(row)

def create_table(connection):
    cursor = connection.cursor()
    cursor.execute("create table if not exists url(time datetime, user text, url text, processed integer)")
    connection.commit()

def insert(connection, user, url):
    cursor = connection.cursor()
    cursor.execute("insert into url (time, user, url, processed) values (datetime('now','localtime'), ?, ?, 0)", (user, url))
    connection.commit()

conn = connect_database(DB_FILE)
create_table(conn)
insert(conn, "foo", "bar")
select_all(conn)
conn.close()
