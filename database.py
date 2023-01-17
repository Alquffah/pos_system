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
            name TEXT,
            email TEXT,
            phone TEXT,
            address TEXT
        )""")

    def delete_table(self, table):
        self.cursor.execute("DROP TABLE {}".format(table))
        self.conn.commit()

    def delete_row(self, table, id):
        self.cursor.execute("DELETE from {} WHERE oid = (?)".format(table), [id])
        self.conn.commit()

    def records(self, table):
        self.cursor.execute("SELECT *, oid FROM {}".format(table))
        return self.cursor.fetchall()

    def find_record(self, table, parameter, value):
        self.cursor.execute("SELECT * FROM {} WHERE {} = (?)".format(table, parameter), value)
        return self.cursor.fetchall()

    def __del__(self):
        self.conn.close()


#c = sqlite3.connect(':memory:') # database in memory
@dataclass
class Item:
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
    name: str
    email: str
    phone: str
    address: str

    def run_query(self, query, parameters = ()):
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    def add_customer(self):
        query = "INSERT INTO customers (name, email, phone, address) VALUES (?,?,?,?)"
        parameters = (self.name, self.email, self.phone, self.address)
        self.run_query(query, parameters)

    def edit_customer(self):
        query = "UPDATE customers SET name = ?, email = ?, phone = ?, address = ? WHERE oid = ?"
        parameters = (self.name, self.email, self.phone, self.address)
        self.run_query(query, parameters)


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
#table().delete_table("customers")
#table().create_customers_table()
#print(table().records("customers"))