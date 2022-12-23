import sqlite3

#c = sqlite3.connect(':memory:') # database in memory
class Product:
    db_name = 'database.db'
    def __init__(self, name, sale, cost, profit, qua, barcode):
        self.name = name
        self.sale = sale
        self.cost = cost
        self.qua = qua
        self.barcode = barcode
        self.profit = profit

    def qua_edit(self, num):
        self.qua += num

    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
            #conn.close()
        return result

    def add_item(self):
        query = "INSERT INTO items (name, price, cost, profit, quantity, bar_code) VALUES (?,?,?,?,?,?)"
        #query = "INSERT INTO products VALUES (?,?,?,?,?,?)"
        parameters = (self.name, self.sale, self.cost, self.profit, self.qua, self.barcode)
        self.run_query(query, parameters)

"""
p1 = Product('cleaner', 6, 4, 2, 12, 123456789012)
#p1.qua_edit(3)
p1.add_item()
"""
