import tkinter as tk
import sqlite3

# Create the main window
window = tk.Tk()

# Set the window title
window.title("My Tkinter Window")

# Create a frame to hold the input boxes
frame = tk.Frame(window)
frame.pack()

# Create the input boxes
input_boxes = []
for i in range(6):
    input_box = tk.Entry(frame)
    input_box.pack(side="left")
    input_boxes.append(input_box)
print(input_boxes)
# Define a function to store the data in the database
def store_data():
    # Connect to the database
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    # Create a table to store the data
    c.execute("CREATE TABLE IF NOT EXISTS data (input1 text, input2 text, input3 text, input4 text, input5 text, input6 text)")

    # Get the data from the input boxes
    data = [input_box.get() for input_box in input_boxes]

    # Insert the data into the table
    c.execute("INSERT INTO data VALUES (?, ?, ?, ?, ?, ?)", data)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

# Create a button to store the data
button = tk.Button(window, text="Store Data", command=store_data)
button.pack()

# Run the main loop to display the window
window.mainloop()
