import sqlite3
from tkinter import *
from tkinter import messagebox

# Database initialization
def initialize_db():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS inventory 
                 (id INTEGER PRIMARY KEY, name TEXT, quantity INTEGER)''')
    conn.commit()
    conn.close()

# Adding a product to the database
def add_product():
    name = entry_name.get()
    quantity = entry_quantity.get()

    if name and quantity:
        conn = sqlite3.connect('inventory.db')
        c = conn.cursor()
        c.execute("INSERT INTO inventory (name, quantity) VALUES (?, ?)", (name, quantity))
        conn.commit()
        conn.close()
        entry_name.delete(0, END)
        entry_quantity.delete(0, END)
        display_inventory()
    else:
        messagebox.showwarning("Input Error", "Please enter product name and quantity.")

# Updating a product's quantity
def update_product():
    try:
        product_id = entry_id.get()
        new_quantity = entry_quantity.get()

        if product_id and new_quantity:
            conn = sqlite3.connect('inventory.db')
            c = conn.cursor()
            c.execute("UPDATE inventory SET quantity = ? WHERE id = ?", (new_quantity, product_id))
            conn.commit()
            conn.close()
            display_inventory()
        else:
            messagebox.showwarning("Input Error", "Please enter product ID and new quantity.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Deleting a product from the database
def delete_product():
    try:
        product_id = entry_id.get()

        if product_id:
            conn = sqlite3.connect('inventory.db')
            c = conn.cursor()
            c.execute("DELETE FROM inventory WHERE id = ?", (product_id,))
            conn.commit()
            conn.close()
            display_inventory()
        else:
            messagebox.showwarning("Input Error", "Please enter product ID to delete.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Displaying the inventory in the text area
def display_inventory():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute("SELECT * FROM inventory")
    rows = c.fetchall()
    conn.close()

    text_area.delete(1.0, END)
    for row in rows:
        text_area.insert(END, f"ID: {row[0]} | Name: {row[1]} | Quantity: {row[2]}\n")

# GUI setup
root = Tk()
root.title("Inventory Management System")

# Labels
Label(root, text="Product ID:").grid(row=0, column=0)
Label(root, text="Product Name:").grid(row=1, column=0)
Label(root, text="Quantity:").grid(row=2, column=0)

# Entry widgets
entry_id = Entry(root)
entry_id.grid(row=0, column=1)
entry_name = Entry(root)
entry_name.grid(row=1, column=1)
entry_quantity = Entry(root)
entry_quantity.grid(row=2, column=1)

# Buttons
Button(root, text="Add Product", command=add_product).grid(row=3, column=0, pady=10)
Button(root, text="Update Quantity", command=update_product).grid(row=3, column=1)
Button(root, text="Delete Product", command=delete_product).grid(row=3, column=2)

# Text area to display inventory
text_area = Text(root, width=50, height=10)
text_area.grid(row=4, column=0, columnspan=3, pady=10)

# Initialize database and display initial inventory
initialize_db()
display_inventory()

# Run the application
root.mainloop()
