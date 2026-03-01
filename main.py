import tkinter as tk
from tkinter import messagebox
import base64

# ---------------- Encryption ----------------
def encrypt(text):
    return base64.b64encode(text.encode()).decode()

def decrypt(text):
    return base64.b64decode(text.encode()).decode()

FILE_NAME = "passwords.txt"

# ---------------- File Helpers ----------------
def read_accounts():
    accounts = []
    try:
        with open(FILE_NAME, "r") as file:
            for line in file:
                website, username, enc_pass = line.strip().split(" | ")
                accounts.append((website, username, enc_pass))
    except FileNotFoundError:
        pass
    return accounts

def write_accounts(accounts):
    with open(FILE_NAME, "w") as file:
        for acc in accounts:
            file.write(" | ".join(acc) + "\n")

# ---------------- GUI Functions ----------------
def add_account():
    website = website_entry.get()
    username = username_entry.get()
    password = password_entry.get()

    if not website or not username or not password:
        messagebox.showwarning("Error", "All fields are required!")
        return

    encrypted_password = encrypt(password)

    with open(FILE_NAME, "a") as file:
        file.write(f"{website} | {username} | {encrypted_password}\n")

    messagebox.showinfo("Success", "Account added successfully!")
    clear_fields()
    refresh_list()

def view_account():
    selected = listbox.curselection()
    if not selected:
        messagebox.showwarning("Error", "Select an account first!")
        return

    index = selected[0]
    accounts = read_accounts()
    website, username, enc_pass = accounts[index]
    password = decrypt(enc_pass)

    messagebox.showinfo(
        "Account Details",
        f"Website: {website}\nUsername: {username}\nPassword: {password}"
    )

def delete_account():
    selected = listbox.curselection()
    if not selected:
        messagebox.showwarning("Error", "Select an account to delete!")
        return

    index = selected[0]
    accounts = read_accounts()
    del accounts[index]
    write_accounts(accounts)
    messagebox.showinfo("Deleted", "Account deleted successfully!")
    refresh_list()

def clear_fields():
    website_entry.delete(0, tk.END)
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)

def refresh_list():
    listbox.delete(0, tk.END)
    accounts = read_accounts()
    for acc in accounts:
        listbox.insert(tk.END, acc[0])  # show website only

# ---------------- GUI Layout ----------------
root = tk.Tk()
root.title("Password Manager")
root.geometry("400x400")

# Labels
tk.Label(root, text="Website:").pack()
website_entry = tk.Entry(root, width=40)
website_entry.pack()

tk.Label(root, text="Username:").pack()
username_entry = tk.Entry(root, width=40)
username_entry.pack()

tk.Label(root, text="Password:").pack()
password_entry = tk.Entry(root, width=40, show="*")
password_entry.pack()

# Buttons
tk.Button(root, text="Add Account", command=add_account).pack(pady=5)
tk.Button(root, text="View Selected", command=view_account).pack(pady=5)
tk.Button(root, text="Delete Selected", command=delete_account).pack(pady=5)
tk.Button(root, text="Clear Fields", command=clear_fields).pack(pady=5)

# Listbox
listbox = tk.Listbox(root, width=50)
listbox.pack(pady=10)
refresh_list()

root.mainloop()
