import sqlite3
conn= sqlite3.connect("db.db")

c=conn.cursor()

c.execute('SELECT name from sqlite_master where type= "table"')

print(c.fetchall())
