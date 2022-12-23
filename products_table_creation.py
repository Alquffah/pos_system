import sqlite3
conn = sqlite3.connect('database.db')
#c = sqlite3.connect(':memory:') # database in memory
c = conn.cursor()
c.execute("""CREATE TABLE items (
    name BLOB,
    price BLOB,
    cost BLOB,
    profit BLOB,
    quantity BLOB,
    bar_code BLOB
)""")

conn.commit()
conn.close()