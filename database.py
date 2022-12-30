from dataclasses import dataclass
import sqlite3

class table:
    def __init__(self):
        self.conn = sqlite3.connect('database.db')
        self.cursor = self.conn.cursor()

    def create_table(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS items (
            name TEXT,
            price REAL,
            cost REAL,
            profit REAL,
            quantity INTEGER,
            bar_code TEXT
        )""")

    def delete_item(self, id):
        self.cursor.execute("DELETE from items WHERE oid = (?)", [id])
        self.conn.commit()

    def records(self):
        self.cursor.execute("SELECT *, oid FROM items")
        return self.cursor.fetchall()

    def __del__(self):
        self.conn.close()

#c = sqlite3.connect(':memory:') # database in memory
@dataclass
class Product:
    name: str
    cost: float
    sale: float
    profit: float
    qua: int
    barcode: str
    id: str

    def qua_edit(self, num):
        self.qua += num

    def run_query(self, query, parameters = ()):
        with sqlite3.connect('database.db') as conn:
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

    def edit_item(self):
        query = "UPDATE items SET name = ?, price = ?, cost = ?, profit = ?, quantity = ?, bar_code = ? WHERE oid = ?"
        parameters = (self.name, self.sale, self.cost, self.profit, self.qua, self.barcode, self.id)
        self.run_query(query, parameters)
 
class customer:
    pass
