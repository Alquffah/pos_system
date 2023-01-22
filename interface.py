import tkinter as tk                    
from tkinter import ttk
import database
import json
import codecs
from datetime import datetime


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
        tab3 = customers(self.notebook)
        tab4 = employees(self.notebook)
        tab5 = history(self.notebook)
        tab6 = analytics(self.notebook)
        tab7 = settings(self.notebook)
        self.notebook.add(tab1,text=langs["tab1"]["title"][configs["lang"]])
        self.notebook.add(tab2,text=langs["tab2"]["title"][configs["lang"]])
        self.notebook.add(tab3,text=langs["tab3"]["title"][configs["lang"]])
        self.notebook.add(tab4,text=langs["tab4"]["title"][configs["lang"]])
        self.notebook.add(tab5,text=langs["tab5"]["title"][configs["lang"]])
        self.notebook.add(tab6,text=langs["tab6"]["title"][configs["lang"]])
        self.notebook.add(tab7,text=langs["tab7"]["title"][configs["lang"]])


class treeview(object):
    def __init__(self, parent, table, entry_boxes):
        self.parent = parent
        self.table = table
        self.entry_boxes = entry_boxes
        self.tab = ""
        #self.cur_item = None
        self.switcher()
        self.create_treeview()

    def create_treeview(self):
        columns_headers = [x for x in langs[self.tab]["data_tree_clmns"]]
        # create the treeview with columns from columns_headers
        self.data_tree = ttk.Treeview(self.parent, columns=columns_headers)
        # make use of the the defualt first column and assign it as the id of the row
        self.data_tree.column("#0", width = 50)
        self.data_tree.heading("#0", text = "id")
        # create the rest of the columns
        for i in columns_headers:
            self.data_tree.column(i, anchor='c', width=90)
            self.data_tree.heading(i, text=langs[self.tab]["data_tree_clmns"][i][configs["lang"]])
        
        self.data_tree.bind('<ButtonRelease-1>', self.select)

        self.data_tree.grid(row = 0, column= 0, rowspan = 6, columnspan=6, padx=20, pady=10, sticky="EW")

        self.show_database()

        
    def show_database(self):
        self.data_tree.delete(*self.data_tree.get_children())
        items_list = database.table().records(self.table)
        for record in items_list:
            self.data_tree.insert(parent='', index='end', text=record[-1], values=[x for x in record[:-1]])

    def show_database_limited(self):
        self.data_tree.delete(*self.data_tree.get_children())
        items_list = database.table().records(self.table)
        print(items_list)
        for record in items_list:
            self.data_tree.insert(parent='', index='end', text=record[-1], values=[record[2], record[2], record[2], record[2], record[2]])

    def store_data(self, source):
        
        
        if self.table == "transactions":
            print(*source[0])
            database.Transaction(1, "time", *source[0], "him", "me", "paid").add_transaction()
            print("yyyyyyyyyyyy")
            self.show_database_limited()

        
        elif self.table == "items":
            source_list = [x.get() for x in source]
            database.item(*source_list).add_item()
            self.show_database()

        elif self.table == "customers":
            source_list = [x.get() for x in source]
            database.customer(*source_list).add_customer()
            self.show_database()

        elif self.table == "employees":
            source_list = [x.get() for x in source]
            database.employee(*source_list).add_employee()
            self.show_database()


    def switcher(self):
        if self.table == "transactions":
            self.tab = "tab1"
        elif self.table == "items":
            self.tab = "tab2"
        elif self.table == "customers":
            self.tab = "tab3"
        elif self.table == "employees":
            self.tab = "tab4" 
       
    def select(self, a):
        curItem = self.data_tree.focus()
        #print(self.data_tree.item(curItem))
        for i, box in enumerate(self.entry_boxes):
            box.delete(0, tk.END)
            box.insert(0, self.data_tree.item(curItem)["values"][i])
            


########################################################################
class cashier(ttk.Frame):
    def __init__(self,*args,**kwargs):
        ttk.Frame.__init__(self,*args,**kwargs)
        self.tab = "tab1"
        # treeview for the items list
        self.data_tree = treeview(self, "transactions", "a")
        # Labels in the Cashier tab 
        #ttk.Label(self, text = langs[self.tab]["current_transaction_lbl"][configs["lang"]]).grid(row = 0, column= 0, columnspan = 8, pady = 20)

        ttk.Label(self, text = langs[self.tab]["total_lbl"][configs["lang"]]).grid(row = 9, column = 6, pady = 20)

        ttk.Label(self, text = langs[self.tab]["cashout_lbl"][configs["lang"]]).grid(row = 11, column = 6, pady = 20)

        self.barcode_not_found_lbl = ttk.Label(self, text = "")
        self.barcode_not_found_lbl.grid(row = 1, column = 11, pady = 5)

        self.cashout_lbl = ttk.Label(self, text = "")
        self.cashout_lbl.grid(row = 11, column = 7, columnspan = 2)

        # buttons in the Cashier tab
        
        add_btn = ttk.Button(self, text = langs[self.tab]["add_btn"][configs["lang"]], command=self.add_item)#, command = self.search_barcode
        add_btn.grid(row = 1, column= 7, pady = 10)

        delete_button = ttk.Button(self, text = langs[self.tab]["delete_btn"][configs["lang"]])#, command = self.delete_item
        delete_button.grid(row = 2, column = 9, pady = 10)

        cashout_button = ttk.Button(self, text = langs[self.tab]["cashin_btn"][configs["lang"]])#, command = self.cashout
        cashout_button.grid(row = 10, column = 6, pady = 10)

        # entry boxes in the Cashier tab
        self.barcode_entry = ttk.Entry(self, width = 15)
        self.barcode_entry.grid(row = 1, column = 6, padx = 10)

        self.total_transaction_var = tk.DoubleVar()
        self.cashin_var = tk.DoubleVar()
        self.total_transaction = ttk.Entry(self, width = 20, textvariable = self.total_transaction_var, state="readonly")
        self.total_transaction.grid(row = 9, column= 7, padx = 10, pady=10)

        self.cashin = ttk.Entry(self, width = 20, textvariable = self.cashin_var)
        self.cashin.grid(row = 10, column= 7, padx = 10, pady=10)


        self.listbox = tk.Listbox(self)
        self.listbox.grid(row = 10, column =1)

        # update the total_transaction entry box
        #self.total_transaction_var.set(self.transaction_total())

    def generate_transaction_id(self):
        trans_id = 1
        while database.table().find_record("transactions", "id", trans_id):
            trans_id += 1
        return trans_id

    dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
       
    def add_item(self):
        # get the barcode number from the entry box
        barcode = self.barcode_entry.get()
        # find the item in the database that corresponds to the barcode
        record = database.table().find_record("items", "bar_code", barcode)
        # add the item to the data tree
        # if the barcode is not found, the database.table.find_item function will return an empty list
        if record:
            self.data_tree.store_data(record)
            #self.data_tree.insert(parent='', index='end', text='', values=(record[0][0], record[0][2], 1, record[0][2], barcode))
        else:
            self.barcode_not_found_lbl.config(text = langs[self.tab]["invalid_barcode_lbl"][configs["lang"]])


    """
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
        record = database.table().find_record("items", "bar_code", barcode)
        # add the item to the data tree
        # if the barcode is not found, the database.table.find_item function will return an empty list
        if record:
            self.data_tree.insert(parent='', index='end', text='', values=(record[0][0], record[0][2], 1, record[0][2], barcode))
        else:
            self.barcode_not_found_lbl.config(text = langs[self.tab]["invalid_barcode_lbl"][configs["lang"]])


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
    """

########################################################################
class items_database(ttk.Frame):
    def __init__(self,*args,**kwargs):
        ttk.Frame.__init__(self,*args,**kwargs)
        self.tab = "tab2"
        #self.name = name
        self.selected_item_id = None

        # Labels in the Database tab
        input_boxes_lbls = ["item_name_lbl", "cost_lbl", "price_lbl", "profit_lbl", "qua_lbl", "barcode_lbl"]
        for i, label in enumerate(input_boxes_lbls):
            ttk.Label(self, text = langs[self.tab][label][configs["lang"]]).grid(row = 0, column= i, padx = 10)

        ttk.Label(self, text = langs[self.tab]["Products Database_lbl"][configs["lang"]], font= 30).grid(row = 3, column= 0, columnspan = 6)
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
        clear_button = ttk.Button(self, text = langs[self.tab]["clear_btn"][configs["lang"]], command=self.clear_entries)
        clear_button.grid(row = 2, column= 1, pady = 10)

        submit_button = ttk.Button(self, text = langs[self.tab]["add_btn"][configs["lang"]], command=self.store_data)
        submit_button.grid(row = 2, column= 0, pady = 10)

        delete_button = ttk.Button(self, text = langs[self.tab]["delete_btn"][configs["lang"]], command=self.delete_item1)
        delete_button.grid(row = 5, column= 0, pady = 10)

        edit_button = ttk.Button(self, text = langs[self.tab]["submit_btn"][configs["lang"]], command=self.edit_item1)
        edit_button.grid(row = 2, column= 2, pady = 10)

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
        database.Item(self.item_name_input.get(), self.item_cost_input.get(), self.item_sale_input.get(), self.item_profit_input.get(), self.item_qua_input.get(), self.item_barcode_input.get(), "").add_item()
        message = langs[self.tab]["added_lbl_1"][configs["lang"]] + str(self.item_name_input.get()) + langs[self.tab]["added_lbl_2"][configs["lang"]]
        self.added_label.config(text = message)
        self.show_database()
      
    def create_data_tree(self):
        #Treeview in the Database view
        coulmns_headers = [x for x in langs[self.tab]["data_tree_clmns"]]
        self.data_tree = ttk.Treeview(self, columns=coulmns_headers)
        self.data_tree.column("#0", width = 0)
        for i in coulmns_headers:
            self.data_tree.column(i, anchor='c', width=100, stretch=False)
            self.data_tree.heading(i, text=langs[self.tab]["data_tree_clmns"][i][configs["lang"]])
        
        self.data_tree.bind('<ButtonRelease-1>', self.selectItem)
        self.data_tree.grid(row = 4, column= 0, columnspan = 6, padx=20)

        #Scrollbars
        self.verscrlbar = ttk.Scrollbar(self,
                                orient ="vertical",
                                command = self.data_tree.yview)
        self.verscrlbar.grid(row = 4, column= 6, sticky='ns')
        self.data_tree.configure(yscrollcommand = self.verscrlbar.set)
        self.data_tree.configure(selectmode="extended")

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
        database.table().delete_row("items", self.selected_item_id)

    def edit_item1(self):
        database.Item(self.item_name_input.get(), self.item_cost_input.get(), self.item_sale_input.get(), self.item_profit_input.get(), self.item_qua_input.get(), self.item_barcode_input.get(), self.selected_item_id).edit_item()
        self.added_label.config(text = langs["tab2"]["editted_lbl"][configs["lang"]])
        self.show_database()
    """
    def item_history_window(self):

        newWindow = tk.Toplevel(my_app)

        newWindow.title("Item History")
    
        newWindow.geometry("550x200")
        """

########################################################################
class customers(ttk.Frame):
    def __init__(self,*args,**kwargs):
        ttk.Frame.__init__(self,*args,**kwargs)
        self.tab = "tab3"
        self.added_label = ttk.Label(self, text ="")
        self.added_label.grid(row = 7, column= 5, columnspan = 5)

        

        self.input_boxes = []
        for i, label in enumerate(langs[self.tab]["data_tree_clmns"]):
            ttk.Label(self, text = langs[self.tab]["data_tree_clmns"][label][configs["lang"]]).grid(row = 6, column= i, padx = 20)
            self.box = ttk.Entry(self, width = 10)
            self.box.grid(row = 7, column= i, padx = 20)
            self.input_boxes.append(self.box)

        self.data_tree = treeview(self, "customers", self.input_boxes)
        add_btn = ttk.Button(self, text = langs[self.tab]["add_btn"][configs["lang"]], command=lambda: self.data_tree.store_data(self.input_boxes))
        add_btn.grid(row = 7, column= 4, padx = 20)



########################################################################
class employees(ttk.Frame):
    def __init__(self,*args,**kwargs):
        ttk.Frame.__init__(self,*args,**kwargs)
        self.tab = "tab4"

        

        self.input_boxes = []
        self.grid_rowconfigure(0, weight = 0)
        self.grid_columnconfigure(0, weight = 0)
        #self.grid_columnconfigure(1, weight = 1)

        for i, label in enumerate(langs[self.tab]["data_tree_clmns"]):
            j = 7
            k = i
            if i > 4:
                j = 9
                k -= 5
            ttk.Label(self, text = langs[self.tab]["data_tree_clmns"][label][configs["lang"]]).grid(row = j, column= k, padx = 10)
            self.box = ttk.Entry(self, width = 10)
            self.box.grid(row = j+1, column= k, padx = 10)
            self.input_boxes.append(self.box)

        self.data_tree = treeview(self, "employees", self.input_boxes)

        add_btn = ttk.Button(self, text = langs[self.tab]["add_btn"][configs["lang"]], command=lambda: self.data_tree.store_data(self.input_boxes))
        add_btn.grid(row = 11, column= 0, padx = 20, pady=20)

        start_shift_btn = ttk.Button(self, text = langs[self.tab]["start_shift_btn"][configs["lang"]], command=self.set_employee)
        start_shift_btn.grid(row = 11, column= 1, padx = 20, pady=20)

    def set_employee(self):
        configs["employee_on_shift"] = self.input_boxes[0].get()
        with open('configs.json', 'w') as f:
            json.dump(configs, f)
        restart()

        #self.horscrlbar = ttk.Scrollbar(self, orient ="horizontal", command = self.data_tree.xview)
        #self.data_tree.configure(xscrollcommand = self.horscrlbar.set)
        #self.horscrlbar.grid(row = 6, column= 0, columnspan = 6, sticky=tk.E +tk.W + tk.N) 


########################################################################
class history(ttk.Frame):
   def __init__(self,*args,**kwargs):
       ttk.Frame.__init__(self,*args,**kwargs)
       self.tab = "tab5"



########################################################################
class analytics(ttk.Frame):
   def __init__(self,*args,**kwargs):
       ttk.Frame.__init__(self,*args,**kwargs)
       self.tab = "tab6"


########################################################################
class settings(ttk.Frame):
    def __init__(self,*args,**kwargs):
        ttk.Frame.__init__(self,*args,**kwargs)
        self.tab = "tab7"

        self.lang_var = tk.IntVar(self, configs["lang"]) # reason for configs["lang"] is to highlight the current radio button setting
        ttk.Label(self, text = langs[self.tab]["choose_lang_lbl"][configs["lang"]]).grid(row = 0, column= 0)

        self.english_rbutton = tk.Radiobutton(self, text = langs[self.tab]["en_rbtn"][configs["lang"]], variable = self.lang_var, value = 0)

        self.english_rbutton.grid(row=1,column=0)

        self.arabic_rbutton = tk.Radiobutton(self, text = langs[self.tab]["ar_rbtn"][configs["lang"]], variable = self.lang_var, value = 1)

        self.arabic_rbutton.grid(row=2,column=0)

        restart_button = ttk.Button(self, text = langs[self.tab]["restart_btn"][configs["lang"]], command=self.change_lang)
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
    employee_on_shift = configs["employee_on_shift"]
    my_app.title(" POS System :     " + str(employee_on_shift))
    my_app.geometry("1000x700")
    my_app.mainloop()

my_app = App()
employee_on_shift = configs["employee_on_shift"]
my_app.title(" POS System :     " + str(employee_on_shift))
my_app.geometry("1000x700")
#my_app.attributes('-fullscreen', True)
# my_app.resizable(0,0) # fix window size

my_app.mainloop()
