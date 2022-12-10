import sqlite3
conn = sqlite3.connect('product.db')
#c = sqlite3.connect(':memory:') # database in memory
c = conn.cursor()

c.execute("SELECT * FROM products")

print(c.fetchall())

conn.commit()
conn.close()