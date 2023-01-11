from dataclasses import dataclass
import sqlite3

class table:
    def __init__(self):
        self.conn = sqlite3.connect('database.db')
        self.cursor = self.conn.cursor()

    def create_items_table(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS items (
            name TEXT,
            cost REAL,
            price REAL,
            profit REAL,
            quantity INTEGER,
            bar_code TEXT
        )""")

    def create_transactions_table(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER,
            time TEXT,
            item_name TEXT,
            item_cost REAL,
            item_sale REAL,
            item_quantity INTEGER,
            item_total_profit REAL,
            item_barcode TEXT,
            customer_id TEXT,
            employee_id TEXT,
            status TEXT
        )""")

    def create_employees_table(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS employees (
            id INTEGER,
            name TEXT,
            position TEXT,
            employment_type TEXT,
            salary REAL,
            date_of_birth TEXT,
            email TEXT,
            phone TEXT,
            address TEXT,
            date_joined TEXT,
            date_left TEXT
        )""")

    def create_customers_table(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS customers (
            id INTEGER,
            name TEXT,
            email TEXT,
            phone TEXT,
            address TEXT
        )""")

    def delete_table(self, table):
        self.cursor.execute("DROP TABLE {}".format(table))
        self.conn.commit()

    def delete_item(self, id):
        self.cursor.execute("DELETE from items WHERE oid = (?)", [id])
        self.conn.commit()

    def records(self, name):
        self.cursor.execute("SELECT *, oid FROM {}".format(name))
        return self.cursor.fetchall()

    def find_item(self, barcode):
        self.cursor.execute("SELECT * FROM items WHERE bar_code = (?)", barcode)
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
        query = "INSERT INTO items (name, cost, price, profit, quantity, bar_code) VALUES (?,?,?,?,?,?)"
        #query = "INSERT INTO products VALUES (?,?,?,?,?,?)"
        parameters = (self.name, self.cost, self.sale, self.profit, self.qua, self.barcode)
        self.run_query(query, parameters)

    def edit_item(self):
        query = "UPDATE items SET name = ?, cost = ?, price = ?, profit = ?, quantity = ?, bar_code = ? WHERE oid = ?"
        parameters = (self.name, self.cost, self.sale, self.profit, self.qua, self.barcode, self.id)
        self.run_query(query, parameters)




@dataclass
class Transaction:
    id: int
    time: str
    item_name: str
    item_cost: float
    item_sale: float
    item_qua: int
    item_total_profit: float
    item_barcode: str
    customer_id: str
    employee_id: str
    status: str # paid fully by the customer or has been added as debt
   
@dataclass
class customer:
    id: int
    name: str
    email: str
    phone: str
    address: str

@dataclass
class employee:
    id: int
    name: str
    position: str
    employment_type: str  # full or part time, contract, etc...
    salary: float
    date_of_birth: str
    email: str
    phone: str
    address: str
    date_joined: str
    date_left: str



#table().create_customers_table()
#print(table().records('items'))
#print(table().find_item('4'))
#table().delete_table("transactions")