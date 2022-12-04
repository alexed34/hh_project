import sqlite3


conn = sqlite3.connect('vacansis.db')
cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS vacans(
   id INT PRIMARY KEY,
   fname TEXT,
   lname TEXT,
   gender TEXT);
""")
conn.commit()
