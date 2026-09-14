import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'foodie.db')

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    c = conn.cursor()
    
    # Users Table
    c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT DEFAULT 'customer',
        loyalty_points INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Addresses Table
    c.execute('''
    CREATE TABLE IF NOT EXISTS addresses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        label TEXT,
        address TEXT NOT NULL,
        is_default BOOLEAN DEFAULT 0,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    ''')

    # Foods Table
    c.execute('''
    CREATE TABLE IF NOT EXISTS foods (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        category TEXT,
        is_veg BOOLEAN,
        rating REAL DEFAULT 0,
        reviews INTEGER DEFAULT 0,
        prep_time INTEGER,
        popularity INTEGER DEFAULT 0,
        description TEXT,
        calories INTEGER,
        discount_percent INTEGER DEFAULT 0,
        bestseller_badge BOOLEAN DEFAULT 0,
        tags TEXT,
        nutrition_protein TEXT,
        nutrition_carbs TEXT,
        nutrition_fat TEXT,
        image_url TEXT,
        is_active BOOLEAN DEFAULT 1
    )
    ''')

    # Orders Table
    c.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        id TEXT PRIMARY KEY,
        user_id INTEGER,
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        subtotal REAL,
        tax REAL,
        delivery_fee REAL,
        discount REAL,
        total REAL,
        status TEXT,
        delivery_address TEXT,
        payment_method TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    ''')

    # Order Items Table
    c.execute('''
    CREATE TABLE IF NOT EXISTS order_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id TEXT,
        food_id INTEGER,
        quantity INTEGER,
        price REAL,
        FOREIGN KEY(order_id) REFERENCES orders(id),
        FOREIGN KEY(food_id) REFERENCES foods(id)
    )
    ''')

    # Wishlist Table
    c.execute('''
    CREATE TABLE IF NOT EXISTS wishlist (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        food_id INTEGER,
        FOREIGN KEY(user_id) REFERENCES users(id),
        FOREIGN KEY(food_id) REFERENCES foods(id),
        UNIQUE(user_id, food_id)
    )
    ''')

    # Coupons Table
    c.execute('''
    CREATE TABLE IF NOT EXISTS coupons (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT UNIQUE NOT NULL,
        discount_percent INTEGER,
        fixed_discount REAL,
        min_order_amount REAL,
        max_discount REAL,
        is_active BOOLEAN DEFAULT 1,
        expiry_date TIMESTAMP
    )
    ''')

    # Notifications Table
    c.execute('''
    CREATE TABLE IF NOT EXISTS notifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        message TEXT,
        is_read BOOLEAN DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    ''')

    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")
