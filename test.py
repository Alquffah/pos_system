import sqlite3

#c = sqlite3.connect(':memory:') # database in memory
class Product:
    db_name = 'product.db'
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

    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    def add_item(self):
        query = "INSERT INTO products (name, price, cost, profit, quantity, bar_code) VALUES (?,?,?,?,?,?)"
        parameters = (p1.name, p1.sale, p1.cost, p1.profit(), p1.qua, p1.barcode)
        self.run_query(query, parameters)


p1 = Product('cleaner', 6, 4, 12, 123456789012)
#p1.qua_edit(3)
p1.add_item()