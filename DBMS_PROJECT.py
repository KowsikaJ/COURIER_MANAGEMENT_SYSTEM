#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import mysql.connector

# Establish a connection to MySQL server
mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Kowsi@0502'
)

cur = mydb.cursor()

# Create database
cur.execute("CREATE DATABASE IF NOT EXISTS courier")

# Connect to the newly created database
mydb.database = 'courier'

# Create tables
cur.execute("""
CREATE TABLE IF NOT EXISTS customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    registration_no VARCHAR(50) UNIQUE,
    phone_number BIGINT,
    password VARCHAR(255)
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS courier (
    courier_id INT AUTO_INCREMENT PRIMARY KEY,
    sender_id INT,
    receiver_name VARCHAR(50),
    receiver_address VARCHAR(255),
    receiver_phone_number BIGINT,
    status VARCHAR(50),
    FOREIGN KEY (sender_id) REFERENCES customers(customer_id)
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS tracking (
    tracking_id INT AUTO_INCREMENT PRIMARY KEY,
    courier_id INT,
    location VARCHAR(255),
    distance_traveled FLOAT,
    status VARCHAR(50),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (courier_id) REFERENCES courier(courier_id)
)
""")

print("Database and tables created successfully!")


# In[ ]:


import mysql.connector
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image

# Database connection and setup
def setup_database():
    mydb = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Keerthana@04'
    )

    cur = mydb.cursor()

    # Create database
    cur.execute("CREATE DATABASE IF NOT EXISTS courier")

    # Connect to the newly created database
    mydb.database = 'courier'

    # Create tables
    cur.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        customer_id INT AUTO_INCREMENT PRIMARY KEY,
        first_name VARCHAR(50),
        last_name VARCHAR(50),
        registration_no VARCHAR(50) UNIQUE,
        phone_number BIGINT,
        password VARCHAR(255)
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS couriers (
        courier_id INT AUTO_INCREMENT PRIMARY KEY,
        sender_id INT,
        receiver_name VARCHAR(50),
        receiver_address VARCHAR(255),
        receiver_phone_number BIGINT,
        status VARCHAR(50),
        FOREIGN KEY (sender_id) REFERENCES customers(customer_id)
    )
    """)

    return mydb, cur

mydb, cur = setup_database()

# Function to insert customer into database
def insert_customer():
    if not (fname.get() and lname.get() and reg_no.get() and phone.get() and password.get() and confirm_password.get()):
        messagebox.showerror('Error', 'All fields are required')
        return

    if password.get() != confirm_password.get():
        messagebox.showerror('Error', 'Passwords do not match')
        return

    cur.execute("""
        INSERT INTO customers (first_name, last_name, registration_no, phone_number, password)
        VALUES (%s, %s, %s, %s, %s)
    """, (fname.get(), lname.get(), reg_no.get(), phone.get(), password.get()))
    
    mydb.commit()
    messagebox.showinfo('Success', 'Registered successfully')
    master.destroy()
    login_page()

# Function to check login credentials
def login_customer():
    cur.execute("""
        SELECT customer_id FROM customers
        WHERE registration_no = %s AND password = %s
    """, (login_reg_no.get(), login_password.get()))
    
    row = cur.fetchone()
    if row:
        customer_id.set(row[0])
        messagebox.showinfo('Success', 'Login successful')
        master.destroy()
        main_page()
    else:
        messagebox.showerror('Error', 'Invalid Registration Number or Password')

# Function to track courier
def track_courier():
    cur.execute("""
        SELECT c.courier_id, c.status, s.first_name, s.last_name, s.phone_number,
               c.receiver_name, c.receiver_address, c.receiver_phone_number
        FROM couriers c
        JOIN customers s ON c.sender_id = s.customer_id
        WHERE c.courier_id = %s
    """, (track_courier_id.get(),))
    
    row = cur.fetchone()
    if row:
        status = f"Status: {row[1]}\nSender: {row[2]} {row[3]}, {row[4]}\nReceiver: {row[5]}, {row[6]}, {row[7]}"
        messagebox.showinfo('Courier Status', status)
    else:
        messagebox.showerror('Error', 'Courier not found')

# Function to insert new courier
def insert_courier():
    cur.execute("""
        INSERT INTO couriers (sender_id, receiver_name, receiver_address, receiver_phone_number, status)
        VALUES (%s, %s, %s, %s, %s)
    """, (customer_id.get(), rec_name.get(), rec_address.get(), rec_phone.get(), 'In Transit'))
    
    mydb.commit()
    messagebox.showinfo('Success', 'Courier added successfully')

# Registration Page
def register_page():
    global master, fname, lname, reg_no, phone, password, confirm_password
    master = Tk()
    master.title("Register")
    master.geometry("400x400")
    
    fname = StringVar()
    lname = StringVar()
    reg_no = StringVar()
    phone = StringVar()
    password = StringVar()
    confirm_password = StringVar()
    
    Label(master, text="First Name").pack()
    Entry(master, textvariable=fname).pack()
    Label(master, text="Last Name").pack()
    Entry(master, textvariable=lname).pack()
    Label(master, text="Registration No").pack()
    Entry(master, textvariable=reg_no).pack()
    Label(master, text="Phone Number").pack()
    Entry(master, textvariable=phone).pack()
    Label(master, text="Password").pack()
    Entry(master, textvariable=password, show='*').pack()
    Label(master, text="Confirm Password").pack()
    Entry(master, textvariable=confirm_password, show='*').pack()
    Button(master, text="Register", command=insert_customer).pack()
    Button(master, text="Login", command=lambda: [master.destroy(), login_page()]).pack()

# Login Page
def login_page():
    global master, login_reg_no, login_password
    master = Tk()
    master.title("Login")
    master.geometry("400x400")
    
    login_reg_no = StringVar()
    login_password = StringVar()
    
    Label(master, text="Registration No").pack()
    Entry(master, textvariable=login_reg_no).pack()
    Label(master, text="Password").pack()
    Entry(master, textvariable=login_password, show='*').pack()
    Button(master, text="Login", command=login_customer).pack()
    Button(master, text="Register", command=lambda: [master.destroy(), register_page()]).pack()

# Main Page
def main_page():
    global master, rec_name, rec_address, rec_phone, track_courier_id
    master = Tk()
    master.title("Courier Management System")
    master.geometry("600x400")
    
    rec_name = StringVar()
    rec_address = StringVar()
    rec_phone = StringVar()
    track_courier_id = StringVar()
    
    Label(master, text="Receiver Name").pack()
    Entry(master, textvariable=rec_name).pack()
    Label(master, text="Receiver Address").pack()
    Entry(master, textvariable=rec_address).pack()
    Label(master, text="Receiver Phone Number").pack()
    Entry(master, textvariable=rec_phone).pack()
    Button(master, text="Add Courier", command=insert_courier).pack()
    
    Label(master, text="Track Courier ID").pack()
    Entry(master, textvariable=track_courier_id).pack()
    Button(master, text="Track", command=track_courier).pack()

    
# Variable to store logged in customer ID
def initialize_customer_id():
    global customer_id
    root = Tk()
    root.withdraw()  # Hide the root window
    customer_id = IntVar(root)
    root.destroy()  # Destroy the hidden root window

initialize_customer_id()

# Start with the login page
login_page()
mainloop()

