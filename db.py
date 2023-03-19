import sqlite3

conn = sqlite3.connect('data.db')
conn.execute('create table count (id INTEGER PRIMARY KEY, k char(255) NOT NULL, v int NOT NULL)')
conn.commit()
