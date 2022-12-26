import tkinter as tk                    
from tkinter import ttk
import database
  
root = tk.Tk(className = " POS System")
root.geometry("700x700")
# root.attributes('-fullscreen', True)
# root.resizable(0,0) # fix window size

# Tabs creation
tabControl = ttk.Notebook(root)
tab1 = ttk.Frame(tabControl)
#tab1.grid(row=3, column=10)
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)
tab4 = ttk.Frame(tabControl)
tabControl.add(tab1, text ='Products Database')
tabControl.add(tab2, text ='Cashier')
tabControl.add(tab3, text ='History')
tabControl.add(tab4, text ='Settings')
tabControl.pack(expand = True, fill ="both")
  
# Item data input section in 1st tab
ttk.Label(tab1, text ="Item Name").grid(row = 0, column= 0, padx = 10)
ttk.Label(tab1, text ="Cost Price").grid(row = 0, column= 1, padx = 10)
ttk.Label(tab1, text ="Sale Price").grid(row = 0, column= 2, padx = 10)
ttk.Label(tab1, text ="Profit").grid(row = 0, column= 3, padx = 10)
ttk.Label(tab1, text ="Quantity").grid(row = 0, column= 4, padx = 10)
ttk.Label(tab1, text ="Barcode").grid(row = 0, column= 5, padx = 10)

name_var, barcode_var = tk.StringVar(), tk.StringVar()
cost_var, sale_var, profit_var, qua_var = tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar(), tk.IntVar()

item_name_input = ttk.Entry(tab1, width = 10, textvariable=name_var)
item_name_input.grid(row = 1, column= 0, padx = 10)

item_cost_input = ttk.Entry(tab1, width = 10, textvariable=cost_var)
item_cost_input.grid(row = 1, column= 1, padx = 10)

item_sale_input = ttk.Entry(tab1, width = 10, textvariable=sale_var)
item_sale_input.grid(row = 1, column= 2, padx = 10)

item_profit_input = ttk.Entry(tab1, width = 10, textvariable=profit_var, state="readonly")
item_profit_input.grid(row = 1, column= 3, padx = 10)

item_qua_input = ttk.Entry(tab1, width = 10, textvariable=qua_var)
item_qua_input.grid(row = 1, column= 4, padx = 10)

item_barcode_input = ttk.Entry(tab1, width = 10, textvariable=barcode_var)
item_barcode_input.grid(row = 1, column= 5, padx = 10)

def calculate_profit(*args):
    global cost_var, sale_var, profit_var

    try:
        # Get sale and cost values (should be integer)
        cost = cost_var.get()
        sale = sale_var.get()
        profit = sale - cost
    except (tk.TclError):
        # In case of invalid input, set profit to 0
        profit = 0
    finally:
        # Set profit
        profit_var.set(profit)


# Trace Od and Do, call count_working_hours on change
cost_var.trace("w", calculate_profit)
sale_var.trace("w", calculate_profit)

def store_data():
    global item_name_input, item_cost_input, item_sale_input, item_profit_input, item_qua_input, item_barcode_input
    database.Product(item_name_input.get(), item_cost_input.get(), item_sale_input.get(), item_profit_input.get(), item_qua_input.get(), item_barcode_input.get()).add_item()
    message = "Added " + str(item_name_input.get()) + " to the database"
    ttk.Label(tab1, text =message).grid(row = 2, column= 3, columnspan = 5)
    show_database()

submit_button = ttk.Button(tab1, text = "Add", command=store_data)
submit_button.grid(row = 2, column= 0, pady = 10)

def clear_entries():
	# Clear entry boxes
	item_name_input.delete(0, 'end')
	item_cost_input.delete(0, 'end')
	item_sale_input.delete(0, 'end')
	item_profit_input.delete(0, 'end')
	item_qua_input.delete(0, 'end')
	item_barcode_input.delete(0, 'end')

clear_button = ttk.Button(tab1, text = "Clear", command=clear_entries)
clear_button.grid(row = 2, column= 1, pady = 10)


ttk.Label(tab1, text ="Products Database", font= 30).grid(row = 3, column= 0, columnspan = 6)

data_tree = ttk.Treeview(tab1)
data_tree["columns"] = ("name", "Sale", "Cost", "Profit", "Quantity", "Barcode", "id")
data_tree.column("#0", width = 0)
data_tree.column("name", width = 150)
data_tree.column("Sale", width = 50)
data_tree.column("Cost", width = 50)
data_tree.column("Profit", width = 50)
data_tree.column("Quantity", width = 60)
data_tree.column("Barcode", width = 150)
data_tree.column("id", width = 50)

data_tree.heading("name", text = "item name")
data_tree.heading("Sale", text = "Sale")
data_tree.heading("Cost", text = "Cost")
data_tree.heading("Profit", text = "Profit")
data_tree.heading("Quantity", text = "Quantity")
data_tree.heading("Barcode", text = "Barcode")
data_tree.heading("id", text = "id")

data_tree.grid(row = 4, column= 0, columnspan = 6, padx=20)

def show_database():
    data_tree.delete(*data_tree.get_children())
    items_list = database.records()
    for record in items_list:
        data_tree.insert(parent='', index='end', text='', values=(record[0], record[1], record[2], record[3], record[4], record[5], record[6]))

show_database()

verscrlbar = ttk.Scrollbar(tab1,
                           orient ="vertical",
                           command = data_tree.yview)
verscrlbar.grid(row = 4, column= 6)
 
# Configuring treeview
data_tree.configure(xscrollcommand = verscrlbar.set)

selected_item_id = None

def selectItem(a):
    global selected_item_id
    
    curItem = data_tree.focus()
    selected_item_id = data_tree.item(curItem)["values"][6]

    name_var.set(data_tree.item(curItem)["values"][0])
    cost_var.set(data_tree.item(curItem)["values"][1])
    sale_var.set(data_tree.item(curItem)["values"][2])
    #item_profit_input = data_tree.item(curItem)["values"][3]
    qua_var.set(data_tree.item(curItem)["values"][4])
    barcode_var.set(data_tree.item(curItem)["values"][5])

    print(item_name_input)

data_tree.bind('<ButtonRelease-1>', selectItem)

def delete_item1():
    selected_item = data_tree.selection()[0] ## get selected item
    data_tree.delete(selected_item) 
    #print(selectItem)
    database.delete_item(selected_item_id)  

delete_button = ttk.Button(tab1, text = "Delete", command=delete_item1)
delete_button.grid(row = 5, column= 0, pady = 10)

def edit_item1():
    global item_name_input, item_cost_input, item_sale_input, item_profit_input, item_qua_input, item_barcode_input

    database.edit_item(item_name_input.get(), item_cost_input.get(), item_sale_input.get(), item_profit_input.get(), item_qua_input.get(), item_barcode_input.get(), selected_item_id)

    show_database()

edit_button = ttk.Button(tab1, text = "Submit Edit", command=edit_item1)
edit_button.grid(row = 2, column= 2, pady = 10)

def item_history_window():

    newWindow = tk.Toplevel(root)

    newWindow.title("Item History")
 
    newWindow.geometry("550x200")

edit_button = ttk.Button(tab1, text = "View history", command=item_history_window)
edit_button.grid(row = 5, column= 1, pady = 10)

root.mainloop()