# check_db.py
import sqlite3

conn = sqlite3.connect("schemes.db")
c = conn.cursor()

c.execute("SELECT name, state, crop FROM schemes")
rows = c.fetchall()

for r in rows:
    print(r)

conn.close()