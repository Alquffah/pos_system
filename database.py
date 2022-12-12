import sqlite3
conn = sqlite3.connect('product.db')
#c = sqlite3.connect(':memory:') # database in memory
c = conn.cursor()
product_name = 'item1'
product_price = '5'
product_cost = '4'
product_profit = '1'
product_quantity = '10'
product_bar_code = '123456789012'
c.execute("INSERT INTO products (product_name, product_price, product_cost, product_profit, product_quantity, product_bar_code) VALUES (?,?,?,?,?,?)", (product_name, product_price, product_cost, product_profit, product_quantity, product_bar_code))

conn.commit()
conn.close()