import sqlite3
import os

DB_FILE = 'data/sales.db'

class Database:
    def __init__(self):
        os.makedirs(os.path.dirname(DB_FILE), exist_ok=True) 
        self.con =  sqlite3.connect(DB_FILE)
        self.con.execute("PRAGMA foreign_keys = ON;")
        self.create_tables()
    
    def create_tables(self):

        table_user = """
        CREATE TABLE if NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        email TEXT,
        password_hash TEXT,
        is_admin BOOLEAN DEFAULT 0
        )
         """

        self.con.execute(table_user)
        print("Table users CREATED")

        table_sales = """
        CREATE TABLE if NOT EXISTS sales(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        doc TEXT,
        amount REAL,
        timestamp TEXT,
        user_id INTEGER,
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
         """

        self.con.execute(table_sales)
        print("Table sales CREATED")


        table_offers = """
        CREATE TABLE if NOT EXISTS offers(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cif TEXT,
        timestamp TEXT,
        name TEXT,
        address TEXT,
        phone TEXT,
        user_id INTEGER,
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
         """

        self.con.execute(table_offers)


        table_offers_positions = """
        CREATE TABLE if NOT EXISTS offers_positions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        offer_id INTEGER,
        product_code TEXT,
        product_name TEXT,
        quantity REAL,
        unit_price REAL,
        vat REAL,
        FOREIGN KEY (offer_id) REFERENCES offers(id) ON DELETE CASCADE
        )
         """
        self.con.execute(table_offers_positions)
        print("Table offers+offers_pos CREATED")
        self.con.commit()
