import sqlite3
conn = sqlite3.connect('product.db')
#c = sqlite3.connect(':memory:') # database in memory
c = conn.cursor()

c.execute("INSERT INTO products VALUES ('item1', '5', '4', '1', '10')")

conn.commit()
conn.close()