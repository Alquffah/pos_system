import sqlite3
conn = sqlite3.connect('product.db')
#c = sqlite3.connect(':memory:') # database in memory
c = conn.cursor()
c.execute("""CREATE TABLE products (
    name text,
    price real,
    cost real,
    profit real,
    quantity integer,
    bar_code text
)""")

conn.commit()
conn.close()