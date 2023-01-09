import tkinter as tk                    
from tkinter import ttk
import database
import json
import codecs

"""
write data
settings = {"lang": "1", "color": "1"}
with open('configs.json', 'w') as f:
    json.dump(settings, f)

read data
with open('configs.json', 'r') as f:
    settings = json.load(f)

settings["lang"] = "2"
with open('configs.json', 'w') as f:
    json.dump(settings, f)
"""
with codecs.open('langs.json', 'r', 'utf-8') as f:
    langs = json.load(f)

with open('configs.json', 'r') as f:
    configs = json.load(f)


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
        self.notebook.add(tab1,text=langs["tab1"]["title"][configs["lang"]])
        self.notebook.add(tab2,text=langs["tab2"]["title"][configs["lang"]])
        self.notebook.add(tab3,text=langs["tab3"]["title"][configs["lang"]])
        self.notebook.add(tab4,text=langs["tab4"]["title"][configs["lang"]])


class cashier(ttk.Frame):
    def __init__(self,*args,**kwargs):
        ttk.Frame.__init__(self,*args,**kwargs)
        self.create_data_tree()

        # Labels in the Cashier tab 
        ttk.Label(self, text = langs["tab1"]["current_transaction_lbl"][configs["lang"]]).grid(row = 0, column= 0, columnspan = 8, pady = 20)

        ttk.Label(self, text = langs["tab1"]["total_lbl"][configs["lang"]]).grid(row = 9, column = 6, pady = 20)

        ttk.Label(self, text = langs["tab1"]["cashout_lbl"][configs["lang"]]).grid(row = 11, column = 6, pady = 20)

        self.barcode_not_found_lbl = ttk.Label(self, text = "")
        self.barcode_not_found_lbl.grid(row = 1, column = 11, pady = 5)

        self.cashout_lbl = ttk.Label(self, text = "")
        self.cashout_lbl.grid(row = 11, column = 7, columnspan = 2)

        # buttons in the Cashier tab
        add_btn = ttk.Button(self, text = langs["tab1"]["add_btn"][configs["lang"]], command = self.search_barcode)
        add_btn.grid(row = 1, column= 10, pady = 10)

        delete_button = ttk.Button(self, text = langs["tab1"]["delete_btn"][configs["lang"]], command = self.delete_item)
        delete_button.grid(row = 2, column = 9, pady = 10)

        cashout_button = ttk.Button(self, text = langs["tab1"]["cashin_btn"][configs["lang"]], command = self.cashout)
        cashout_button.grid(row = 10, column = 6, pady = 10)

        # entry boxes in the Cashier tab
        self.barcode_entry = ttk.Entry(self, width = 15)
        self.barcode_entry.grid(row = 1, column = 9, padx = 10)

        self.total_transaction_var = tk.DoubleVar()
        self.cashin_var = tk.DoubleVar()
        self.total_transaction = ttk.Entry(self, width = 20, textvariable = self.total_transaction_var, state="readonly")
        self.total_transaction.grid(row = 9, column= 7, padx = 10, pady=10)

        self.cashin = ttk.Entry(self, width = 20, textvariable = self.cashin_var)
        self.cashin.grid(row = 10, column= 7, padx = 10, pady=10)

        # update the total_transaction entry box
        self.total_transaction_var.set(self.transaction_total())
        #self.show_database()


    def delete_item(self):
        self.data_tree.delete(self.data_tree.selection()[0]) 
        # update the total_transaction entry box
        self.total_transaction_var.set(self.transaction_total())


    def search_barcode(self):
        # if the data_tree is empty, then add the item
        if not self.data_tree.get_children():
            self.add_item()
        # else, search the data_tree for the item by the barcode number
        else:  
            for child in self.data_tree.get_children():
                # for every row in the data_tree, compare if the barcode matches with the barcode from the entry box 
                if str(self.barcode_entry.get()) == str(self.data_tree.item(child)['values'][4]):
                    # if true the copy the old (name, price, barcode), increase the quantity by 1 and adjust the total
                    old_name = self.data_tree.item(child)['values'][0]
                    old_price = self.data_tree.item(child)['values'][1]
                    new_qua = self.data_tree.item(child)['values'][2] + 1
                    new_total = float(old_price) * new_qua
                    old_barcode = self.data_tree.item(child)['values'][4]
                    # insert the adjusted values into the data_tree so it refreshes automatically
                    self.data_tree.item(child, text='', values=(old_name, old_price, new_qua, new_total, old_barcode))
                    # update the total_transaction entry box
                    self.total_transaction_var.set(self.transaction_total())
                    return
            # if the search fails to find a matching barcode then add the item to the data_tree
            self.add_item()
        self.total_transaction_var.set(self.transaction_total())


    def add_item(self):
        # get the barcode number from the entry box
        barcode = self.barcode_entry.get()
        # find the item in the database that corresponds to the barcode
        record = database.table().find_item(barcode)
        # add the item to the data tree
        # if the barcode is not found, the database.table.find_item function will return an empty list
        if record:
            self.data_tree.insert(parent='', index='end', text='', values=(record[0][0], record[0][2], 1, record[0][2], barcode))
        else:
            self.barcode_not_found_lbl.config(text = langs["tab1"]["invalid_barcode_lbl"][configs["lang"]])


    def transaction_total(self, item=""):
        sum = 0.0
        for row in self.data_tree.get_children(item):
            sum += float(self.data_tree.item(row)['values'][3])
        return sum


    def cashout(self):
        # triggered by cashout button
        cash = self.cashin_var.get() - self.transaction_total()
        self.cashout_lbl.config(text = str(cash))


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
        self.data_tree["columns"] = ("name", "Price", "Quantity", "Total", "barcode")
        self.data_tree.column("#0", width = 0)
        self.data_tree.column("name", width = 150)
        self.data_tree.column("Price", width = 60)
        self.data_tree.column("Quantity", width = 60)
        self.data_tree.column("Total", width = 150)
        self.data_tree.column("barcode", width = 0)
        self.data_tree.heading("name", text = langs["tab1"]["item_clmn"][configs["lang"]])
        self.data_tree.heading("Price", text = langs["tab1"]["price_clmn"][configs["lang"]])
        self.data_tree.heading("Quantity", text = langs["tab1"]["qua_clmn"][configs["lang"]])
        self.data_tree.heading("Total", text = langs["tab1"]["total_clmn"][configs["lang"]])
        #self.data_tree.bind('<ButtonRelease-1>', self.selectItem)
        self.data_tree.grid(row = 1, column= 0, rowspan = 8, columnspan = 8, padx=20)
        #return self.data_tree
        

class items_database(ttk.Frame):
    def __init__(self,*args,**kwargs):
        ttk.Frame.__init__(self,*args,**kwargs)
        #self.name = name
        self.selected_item_id = None

        # Labels in the Database tab
        ttk.Label(self, text = langs["tab2"]["item_name_lbl"][configs["lang"]]).grid(row = 0, column= 0, padx = 10)
        ttk.Label(self, text = langs["tab2"]["cost_lbl"][configs["lang"]]).grid(row = 0, column= 1, padx = 10)
        ttk.Label(self, text = langs["tab2"]["price_lbl"][configs["lang"]]).grid(row = 0, column= 2, padx = 10)
        ttk.Label(self, text = langs["tab2"]["profit_lbl"][configs["lang"]]).grid(row = 0, column= 3, padx = 10)
        ttk.Label(self, text = langs["tab2"]["qua_lbl"][configs["lang"]]).grid(row = 0, column= 4, padx = 10)
        ttk.Label(self, text = langs["tab2"]["barcode_lbl"][configs["lang"]]).grid(row = 0, column= 5, padx = 10)
        ttk.Label(self, text = langs["tab2"]["Products Database_lbl"][configs["lang"]], font= 30).grid(row = 3, column= 0, columnspan = 6)
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
        clear_button = ttk.Button(self, text = langs["tab2"]["clear_btn"][configs["lang"]], command=self.clear_entries)
        clear_button.grid(row = 2, column= 1, pady = 10)

        submit_button = ttk.Button(self, text = langs["tab2"]["add_btn"][configs["lang"]], command=self.store_data)
        submit_button.grid(row = 2, column= 0, pady = 10)

        delete_button = ttk.Button(self, text = langs["tab2"]["delete_btn"][configs["lang"]], command=self.delete_item1)
        delete_button.grid(row = 5, column= 0, pady = 10)

        edit_button = ttk.Button(self, text = langs["tab2"]["submit_btn"][configs["lang"]], command=self.edit_item1)
        edit_button.grid(row = 2, column= 2, pady = 10)

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
        message = langs["tab2"]["added_lbl_1"][configs["lang"]] + str(self.item_name_input.get()) + langs["tab2"]["added_lbl_2"][configs["lang"]]
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

        self.data_tree.heading("name", text = langs["tab2"]["item_clmn"][configs["lang"]])
        self.data_tree.heading("Cost", text = langs["tab2"]["cost_clmn"][configs["lang"]])
        self.data_tree.heading("Sale", text = langs["tab2"]["price_clmn"][configs["lang"]])
        self.data_tree.heading("Profit", text = langs["tab2"]["profit_clmn"][configs["lang"]])
        self.data_tree.heading("Quantity", text = langs["tab2"]["qua_clmn"][configs["lang"]])
        self.data_tree.heading("Barcode", text = langs["tab2"]["barcode_clmn"][configs["lang"]])
        self.data_tree.heading("id", text = langs["tab2"]["id_clmn"][configs["lang"]])
        

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
        self.added_label.config(text = langs["tab2"]["editted_lbl"][configs["lang"]])
        self.show_database()
    """
    def item_history_window(self):

        newWindow = tk.Toplevel(my_app)

        newWindow.title("Item History")
    
        newWindow.geometry("550x200")
        """
 
class history(ttk.Frame):
   def __init__(self,*args,**kwargs):
       ttk.Frame.__init__(self,*args,**kwargs)


class settings(ttk.Frame):
    def __init__(self,*args,**kwargs):
        ttk.Frame.__init__(self,*args,**kwargs)

        self.lang_var = tk.IntVar(self, configs["lang"]) # reason for configs["lang"] is to highlight the current radio button setting
        ttk.Label(self, text = langs["tab4"]["choose_lang_lbl"][configs["lang"]]).grid(row = 0, column= 0)

        self.english_rbutton = tk.Radiobutton(self, text = langs["tab4"]["en_rbtn"][configs["lang"]], variable = self.lang_var, value = 0)

        self.english_rbutton.grid(row=1,column=0)

        self.arabic_rbutton = tk.Radiobutton(self, text = langs["tab4"]["ar_rbtn"][configs["lang"]], variable = self.lang_var, value = 1)

        self.arabic_rbutton.grid(row=2,column=0)

        restart_button = ttk.Button(self, text = langs["tab4"]["restart_btn"][configs["lang"]], command=self.change_lang)
        restart_button.grid(row = 2, column= 1, pady = 10)

  
    def change_lang(self):
        configs["lang"] = self.lang_var.get()
        with open('configs.json', 'w') as f:
            json.dump(configs, f)
        restart()

def restart():
    global my_app
    my_app.destroy()
    my_app = App()
    my_app.title(" POS System")
    my_app.geometry("1000x700")
    my_app.mainloop()

my_app = App()
my_app.title(" POS System")
my_app.geometry("1000x700")
#my_app.attributes('-fullscreen', True)
# my_app.resizable(0,0) # fix window size

my_app.mainloop()
