import sqlite3
#conn = sqlite3.connect('product.db')
conn = sqlite3.connect('database.db')

#c = sqlite3.connect(':memory:') # database in memory
c = conn.cursor()

#c.execute("SELECT * FROM products")
c.execute("SELECT * FROM items")

print(c.fetchall())

conn.commit()
conn.close()