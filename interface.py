import tkinter as tk                    
from tkinter import ttk
import database


class App(tk.Tk):
    def __init__(self,*args,**kwargs):
        tk.Tk.__init__(self,*args,**kwargs)
        self.notebook = ttk.Notebook()
        self.add_tab()
        self.notebook.grid(row=0)
        
        self.notebook.pack(expand = True, fill ="both")
  
    def add_tab(self):
        tab1 = cashier(self.notebook)
        tab2 = items_database(self.notebook)
        tab3 = history(self.notebook)
        tab4 = settings(self.notebook)
        self.notebook.add(tab1,text="Cashier")
        self.notebook.add(tab2,text="Database")
        self.notebook.add(tab3,text="History")
        self.notebook.add(tab4,text="Settings")

class cashier(ttk.Frame):
    def __init__(self,*args,**kwargs):
        ttk.Frame.__init__(self,*args,**kwargs)
        self.create_data_tree()

        # Labels in the Database tab
        ttk.Label(self, text ="Currant Transaction").grid(row = 0, column= 0, columnspan = 8, pady=20)
        ttk.Label(self, text ="Total").grid(row = 9, column= 6, pady=20)
        #ttk.Label(self, text ="Item Name").grid(row = 1, column= 0, padx = 10, pady=20)

        # buttons
        add_button = ttk.Button(self, text = "Add", command=self.add_item)
        add_button.grid(row = 1, column= 10, pady = 10)

        # entry boxes
        self.barcode_entry = ttk.Entry(self, width = 15)
        self.barcode_entry.grid(row = 1, column= 9, padx = 10)

        self.total_transaction = ttk.Entry(self, width = 20)
        self.total_transaction.grid(row = 9, column= 7, padx = 10, pady=10)

    def add_item(self):
        barcode = self.barcode_entry.get()
        record = database.table().find_item(barcode)
        #print(record[0][0])
        self.data_tree.insert(parent='', index='end', text='', values=(record[0][0], record[0][2], self.quantity_manager(), record[0][2] * self.quantity_manager()))
        #self.show_database()

    def quantity_manager(self):
        qua = 1

        return qua
    def show_database(self):
        pass
        #self.data_tree.delete(*self.data_tree.get_children())
        #items_list = database.table().records('items')
        #for record in items_list:
            #self.data_tree.insert(parent='', index='end', text='', values=(record[0], record[1], record[2], record[3], record[4], record[5], record[6]))

        #self.show_database()
    def create_data_tree(self):
        #Treeview in the Database view
        self.data_tree = ttk.Treeview(self, height=10)
        self.data_tree["columns"] = ("name", "Price", "Quantity", "Total")
        self.data_tree.column("#0", width = 0)
        self.data_tree.column("name", width = 150)
        self.data_tree.column("Price", width = 60)
        self.data_tree.column("Quantity", width = 60)
        self.data_tree.column("Total", width = 150)
        

        self.data_tree.heading("name", text = "Name")
        self.data_tree.heading("Price", text = "Unit Price")
        self.data_tree.heading("Quantity", text = "Quantity")
        self.data_tree.heading("Total", text = "Total Price")

        #self.data_tree.bind('<ButtonRelease-1>', self.selectItem)
        self.data_tree.grid(row = 1, column= 0, rowspan = 8, columnspan = 8, padx=20)
        

        #return self.data_tree
        

class items_database(ttk.Frame):
    def __init__(self,*args,**kwargs):
        ttk.Frame.__init__(self,*args,**kwargs)
        #self.name = name
        self.selected_item_id = None

        # Labels in the Database tab
        ttk.Label(self, text ="Item Name").grid(row = 0, column= 0, padx = 10)
        ttk.Label(self, text ="Cost Price").grid(row = 0, column= 1, padx = 10)
        ttk.Label(self, text ="Sale Price").grid(row = 0, column= 2, padx = 10)
        ttk.Label(self, text ="Profit").grid(row = 0, column= 3, padx = 10)
        ttk.Label(self, text ="Quantity").grid(row = 0, column= 4, padx = 10)
        ttk.Label(self, text ="Barcode").grid(row = 0, column= 5, padx = 10)
        ttk.Label(self, text ="Products Database", font= 30).grid(row = 3, column= 0, columnspan = 6)
        self.added_label = ttk.Label(self, text ="")
        self.added_label.grid(row = 2, column= 3, columnspan = 5)

        #Entry boxes in the Database tab
        self.name_var, self.barcode_var = tk.StringVar(), tk.StringVar()
        self.cost_var, self.sale_var, self.profit_var, self.qua_var = tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar(), tk.IntVar()

        self.item_name_input = ttk.Entry(self, width = 10, textvariable=self.name_var)
        self.item_name_input.grid(row = 1, column= 0, padx = 10)

        self.item_cost_input = ttk.Entry(self, width = 10, textvariable=self.cost_var)
        self.item_cost_input.grid(row = 1, column= 1, padx = 10)

        self.item_sale_input = ttk.Entry(self, width = 10, textvariable=self.sale_var)
        self.item_sale_input.grid(row = 1, column= 2, padx = 10)

        self.item_profit_input = ttk.Entry(self, width = 10, textvariable=self.profit_var, state="readonly")
        self.item_profit_input.grid(row = 1, column= 3, padx = 10)
        # Trace Od and Do, call count_working_hours on change
        self.cost_var.trace("w", self.calculate_profit)
        self.sale_var.trace("w", self.calculate_profit)

        self.item_qua_input = ttk.Entry(self, width = 10, textvariable=self.qua_var)
        self.item_qua_input.grid(row = 1, column= 4, padx = 10)

        self.item_barcode_input = ttk.Entry(self, width = 10, textvariable=self.barcode_var)
        self.item_barcode_input.grid(row = 1, column= 5, padx = 10)

        self.create_data_tree()
        self.show_database()


        #Buttons in the Database tab
        clear_button = ttk.Button(self, text = "Clear", command=self.clear_entries)
        clear_button.grid(row = 2, column= 1, pady = 10)

        submit_button = ttk.Button(self, text = "Add", command=self.store_data)
        submit_button.grid(row = 2, column= 0, pady = 10)

        delete_button = ttk.Button(self, text = "Delete", command=self.delete_item1)
        delete_button.grid(row = 5, column= 0, pady = 10)

        edit_button = ttk.Button(self, text = "Submit Edit", command=self.edit_item1)
        edit_button.grid(row = 2, column= 2, pady = 10)

        #edit_button = ttk.Button(self, text = "View history", command=self.item_history_window)
        #edit_button.grid(row = 5, column= 1, pady = 10)

    #Scrollbars
        self.verscrlbar = ttk.Scrollbar(self,
                                orient ="vertical",
                                command = self.data_tree.yview)
        self.verscrlbar.grid(row = 4, column= 6)
        self.data_tree.configure(xscrollcommand = self.verscrlbar.set)

    #Functions
    def calculate_profit(self, *args):

        try:
            # Get sale and cost values (should be integer)
            cost = self.cost_var.get()
            sale = self.sale_var.get()
            profit = sale - cost
        except (tk.TclError):
            # In case of invalid input, set profit to 0
            profit = 0
        finally:
            # Set profit
            self.profit_var.set(profit)

            
    def clear_entries(self):
        # Clear entry boxes
        self.item_name_input.delete(0, 'end')
        self.item_cost_input.delete(0, 'end')
        self.item_sale_input.delete(0, 'end')
        self.item_profit_input.delete(0, 'end')
        self.item_qua_input.delete(0, 'end')
        self.item_barcode_input.delete(0, 'end')
    
    def store_data(self):
        database.Product(self.item_name_input.get(), self.item_cost_input.get(), self.item_sale_input.get(), self.item_profit_input.get(), self.item_qua_input.get(), self.item_barcode_input.get(), "").add_item()
        message = "Added " + str(self.item_name_input.get()) + " to the database"
        self.added_label.config(text = message)
        self.show_database()
    
    def create_data_tree(self):
        #Treeview in the Database view
        self.data_tree = ttk.Treeview(self)
        self.data_tree["columns"] = ("name", "Cost", "Sale", "Profit", "Quantity", "Barcode", "id")
        self.data_tree.column("#0", width = 0)
        self.data_tree.column("name", width = 150)
        self.data_tree.column("Cost", width = 50)
        self.data_tree.column("Sale", width = 50)
        self.data_tree.column("Profit", width = 50)
        self.data_tree.column("Quantity", width = 60)
        self.data_tree.column("Barcode", width = 150)
        self.data_tree.column("id", width = 50)

        self.data_tree.heading("name", text = "item name")
        self.data_tree.heading("Cost", text = "Cost")
        self.data_tree.heading("Sale", text = "Sale")
        self.data_tree.heading("Profit", text = "Profit")
        self.data_tree.heading("Quantity", text = "Quantity")
        self.data_tree.heading("Barcode", text = "Barcode")
        self.data_tree.heading("id", text = "id")
        

        self.data_tree.bind('<ButtonRelease-1>', self.selectItem)
        self.data_tree.grid(row = 4, column= 0, columnspan = 6, padx=20)
        

        #return self.data_tree

    def show_database(self):
        self.data_tree.delete(*self.data_tree.get_children())
        items_list = database.table().records('items')
        for record in items_list:
            self.data_tree.insert(parent='', index='end', text='', values=(record[0], record[1], record[2], record[3], record[4], record[5], record[6]))
    

    def selectItem(self,a):
        curItem = self.data_tree.focus()
        
        self.name_var.set(self.data_tree.item(curItem)["values"][0])
        self.cost_var.set(self.data_tree.item(curItem)["values"][1])
        self.sale_var.set(self.data_tree.item(curItem)["values"][2])
        self.qua_var.set(self.data_tree.item(curItem)["values"][4])
        self.barcode_var.set(self.data_tree.item(curItem)["values"][5])
        self.selected_item_id = self.data_tree.item(curItem)["values"][6]

    def delete_item1(self):
        selected_item = self.data_tree.selection()[0] # get selected item
        self.data_tree.delete(selected_item) 
        database.table().delete_item(self.selected_item_id)

    def edit_item1(self):
        database.Product(self.item_name_input.get(), self.item_cost_input.get(), self.item_sale_input.get(), self.item_profit_input.get(), self.item_qua_input.get(), self.item_barcode_input.get(), self.selected_item_id).edit_item()
        message = "Editted!"
        self.added_label.config(text = message)
        self.show_database()
    """
    def item_history_window(self):

        newWindow = tk.Toplevel(my_app)

        newWindow.title("Item History")
    
        newWindow.geometry("550x200")
        """
 
class history(ttk.Frame):
   def __init__(self,name,*args,**kwargs):
       ttk.Frame.__init__(self,*args,**kwargs)
       self.label = ttk.Label(self, text="Hi This is Tab3")
       self.label.grid(row=1,column=0,padx=10,pady=10)

class settings(ttk.Frame):
   def __init__(self,name,*args,**kwargs):
       ttk.Frame.__init__(self,*args,**kwargs)
       self.label = ttk.Label(self, text="Hi This is Tab4")
       self.label.grid(row=1,column=0,padx=10,pady=10)

my_app = App()
my_app.title(" POS System")
my_app.geometry("1000x700")
#my_app.attributes('-fullscreen', True)
# my_app.resizable(0,0) # fix window size

my_app.mainloop()
