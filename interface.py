import tkinter as tk                    
from tkinter import ttk
#from tkinter import *
import sqlite3
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
cost_var, sale_var, profit_var, qua_var = tk.IntVar(value=0), tk.IntVar(value=0), tk.IntVar(value=0), tk.IntVar(value=0)

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
    global item_name_input, cost_var, item_sale_input, item_profit_input, item_qua_input, item_barcode_input
    database.Product(item_name_input.get(), item_cost_input.get(), item_sale_input.get(), item_profit_input.get(), item_qua_input.get(), item_barcode_input.get()).add_item()


submit_button = ttk.Button(tab1, text = "Add", command=lambda: store_data())
submit_button.grid(row = 2, column= 0, pady = 10)

ttk.Label(tab2,
          text ="Lets dive into the\
          world of computers").grid(column = 0,
                                    row = 0, 
                                    padx = 30,
                                    pady = 30)
  
root.mainloop()