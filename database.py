import sqlite3
conn = sqlite3.connect('product.db')
#c = sqlite3.connect(':memory:') # database in memory
c = conn.cursor()
class Product:
    def __init__(self, name, sale, cost, qua, barcode):
        self.name = name
        self.sale = sale
        self.cost = cost
        self.qua = qua
        self.barcode = barcode

    def profit(self):
        return self.sale - self.cost

    def qua_edit(self, num):
        self.qua += num

p1 = Product('cleaner', 6, 4, 12, 123456789012)
p1.qua_edit(3)

c.execute("INSERT INTO products (name, price, cost, profit, quantity, bar_code) VALUES (?,?,?,?,?,?)", (p1.name, p1.sale, p1.cost, p1.profit(), p1.qua, p1.barcode))

conn.commit()
conn.close()