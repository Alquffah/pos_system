import sqlite3
conn = sqlite3.connect('database.db')
#c = sqlite3.connect(':memory:') # database in memory
c = conn.cursor()
c.execute("""CREATE TABLE items (
    name TEXT,
    price REAL,
    cost REAL,
    profit REAL,
    quantity INTEGER,
    bar_code TEXT
)""")

conn.commit()
conn.close()