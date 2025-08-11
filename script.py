import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3
import os

DB_FILE = os.path.join(os.path.dirname(__file__), "contacts.db")

# Database setup
def setup_database():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL
            )
        """)
        conn.commit()

def load_contacts():
    contact_list.delete(0, tk.END)
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name, phone FROM contacts")
        for name, phone in cursor.fetchall():
            contact_list.insert(tk.END, f"{name} - {phone}")

def add_contact():
    name = name_entry.get()
    phone = phone_entry.get()
    
    if name and phone:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO contacts (name, phone) VALUES (?, ?)", (name, phone))
            conn.commit()
        load_contacts()
        name_entry.delete(0, tk.END)
        phone_entry.delete(0, tk.END)
    else:
        messagebox.showerror("Oops!", "Please enter both name and phone number. 🌸")

def delete_contact():
    try:
        selected_index = contact_list.curselection()[0]
        selected_contact = contact_list.get(selected_index)
        name, phone = selected_contact.split(" - ")

        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM contacts WHERE name = ? AND phone = ?", (name, phone))
            conn.commit()

        load_contacts()
    except IndexError:
        messagebox.showerror("Uh-oh!", "No contact selected! 🐥")

def clear_contacts():
    result = messagebox.askyesno("Confirm", "Delete ALL contacts? 😱")
    if result:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM contacts")
            conn.commit()
        load_contacts()

def get_selected_contact(event):
    try:
        selected_index = contact_list.curselection()[0]
        selected_contact = contact_list.get(selected_index)
        name, phone = selected_contact.split(" - ")
        name_entry.delete(0, tk.END)
        phone_entry.delete(0, tk.END)
        name_entry.insert(tk.END, name)
        phone_entry.insert(tk.END, phone)
    except IndexError:
        pass


root = tk.Tk()
root.title("🌈 Contact Book")
root.geometry("480x500")
root.config(bg="#FFDFAF")

# Style
style = ttk.Style()
style.theme_use("default")
style.configure("TLabel", background="#FFDFAF", foreground="#444444", font=("Comic Sans MS", 11, "bold"))
style.configure("TEntry", padding=6, font=("Comic Sans MS", 10))
style.configure("CartoonButton.TButton",
                background="#FF8AAE",
                foreground="white",
                font=("Comic Sans MS", 10, "bold"),
                padding=8,
                relief="flat")
style.map("CartoonButton.TButton", background=[("active", "#FF6F91")])

# Top form frame
form_frame = tk.Frame(root, bg="#FFF4D6", bd=3, relief="ridge", padx=10, pady=10)
form_frame.pack(pady=10, padx=10, fill="x")

name_label = ttk.Label(form_frame, text="Name ✏️:")
name_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
name_entry = ttk.Entry(form_frame, width=20)
name_entry.grid(row=0, column=1, padx=5, pady=5)

phone_label = ttk.Label(form_frame, text="Phone 📞:")
phone_label.grid(row=0, column=2, padx=5, pady=5, sticky="w")
phone_entry = ttk.Entry(form_frame, width=20)
phone_entry.grid(row=0, column=3, padx=5, pady=5)

# Button row
button_frame = tk.Frame(root, bg="#FFDFAF")
button_frame.pack(pady=5)

add_button = ttk.Button(button_frame, text="➕ Add", command=add_contact, style="CartoonButton.TButton")
add_button.grid(row=0, column=0, padx=5)

delete_button = ttk.Button(button_frame, text="❌ Delete", command=delete_contact, style="CartoonButton.TButton")
delete_button.grid(row=0, column=1, padx=5)

clear_button = ttk.Button(button_frame, text="🧹 Clear", command=clear_contacts, style="CartoonButton.TButton")
clear_button.grid(row=0, column=2, padx=5)

# Contact list frame
list_frame = tk.LabelFrame(root, text="📜 Contact List", bg="#FFDFAF", font=("Comic Sans MS", 11, "bold"), fg="#444444")
list_frame.pack(padx=10, pady=10, fill="both", expand=True)

contact_list = tk.Listbox(list_frame, height=12, bg="#FFF9E6", fg="#444444", font=("Comic Sans MS", 10),
                          selectbackground="#FF8AAE", selectforeground="#FFFFFF", bd=2, relief="groove", highlightthickness=0)
contact_list.pack(fill="both", expand=True, padx=10, pady=10)

contact_list.bind('<<ListboxSelect>>', get_selected_contact)

setup_database()
load_contacts()

root.mainloop()
