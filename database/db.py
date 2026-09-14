import sqlite3
import os
import hashlib

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'foodie.db')

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(name, email, password, role='customer'):
    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute('INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)',
                  (name, email, hash_password(password), role))
        conn.commit()
        user_id = c.lastrowid
        return get_user(user_id)
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()

def authenticate_user(email, password):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, hash_password(password)))
    user = c.fetchone()
    conn.close()
    if user:
        return dict(user)
    return None

def get_user(user_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = c.fetchone()
    conn.close()
    if user:
        return dict(user)
    return None

def get_foods(category=None, is_veg=None, min_price=None, max_price=None, min_rating=None, search=None, sort_by=None):
    conn = get_connection()
    c = conn.cursor()
    
    query = 'SELECT * FROM foods WHERE is_active = 1'
    params = []
    
    if category:
        query += ' AND category = ?'
        params.append(category)
    if is_veg is not None:
        query += ' AND is_veg = ?'
        params.append(1 if is_veg else 0)
    if min_price is not None:
        query += ' AND price >= ?'
        params.append(min_price)
    if max_price is not None:
        query += ' AND price <= ?'
        params.append(max_price)
    if min_rating is not None:
        query += ' AND rating >= ?'
        params.append(min_rating)
    if search:
        query += ' AND name LIKE ?'
        params.append(f'%{search}%')
        
    if sort_by == 'price_asc':
        query += ' ORDER BY price ASC'
    elif sort_by == 'price_desc':
        query += ' ORDER BY price DESC'
    elif sort_by == 'rating':
        query += ' ORDER BY rating DESC'
    elif sort_by == 'popularity':
        query += ' ORDER BY popularity DESC'
    
    c.execute(query, params)
    foods = [dict(row) for row in c.fetchall()]
    conn.close()
    
    for f in foods:
        if 'tags' in f and f['tags']:
            f['tags'] = f['tags'].split(',')
        else:
            f['tags'] = []
    return foods

def get_food(food_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM foods WHERE id = ?', (food_id,))
    food = c.fetchone()
    conn.close()
    if food:
        food = dict(food)
        if 'tags' in food and food['tags']:
            food['tags'] = food['tags'].split(',')
        else:
            food['tags'] = []
        return food
    return None

def add_to_wishlist(user_id, food_id):
    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute('INSERT INTO wishlist (user_id, food_id) VALUES (?, ?)', (user_id, food_id))
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    finally:
        conn.close()

def remove_from_wishlist(user_id, food_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('DELETE FROM wishlist WHERE user_id = ? AND food_id = ?', (user_id, food_id))
    conn.commit()
    conn.close()

def get_wishlist(user_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT food_id FROM wishlist WHERE user_id = ?', (user_id,))
    items = [row['food_id'] for row in c.fetchall()]
    conn.close()
    return items

def create_order(user_id, order_id, items, subtotal, tax, delivery_fee, discount, total, address, payment_method):
    conn = get_connection()
    c = conn.cursor()
    
    # Insert order
    c.execute('''
    INSERT INTO orders (id, user_id, subtotal, tax, delivery_fee, discount, total, status, delivery_address, payment_method)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (order_id, user_id, subtotal, tax, delivery_fee, discount, total, 'Order Placed', address, payment_method))
    
    # Insert items
    for item in items:
        c.execute('''
        INSERT INTO order_items (order_id, food_id, quantity, price)
        VALUES (?, ?, ?, ?)
        ''', (order_id, item['id'], item['quantity'], item['price']))
        
    conn.commit()
    conn.close()

def get_user_orders(user_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM orders WHERE user_id = ? ORDER BY date DESC', (user_id,))
    orders = [dict(row) for row in c.fetchall()]
    
    for order in orders:
        c.execute('''
        SELECT oi.*, f.name 
        FROM order_items oi
        JOIN foods f ON oi.food_id = f.id
        WHERE oi.order_id = ?
        ''', (order['id'],))
        order['items'] = [dict(row) for row in c.fetchall()]
        
    conn.close()
    return orders

def get_all_orders():
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM orders ORDER BY date DESC')
    orders = [dict(row) for row in c.fetchall()]
    conn.close()
    return orders

def update_order_status(order_id, status):
    conn = get_connection()
    c = conn.cursor()
    c.execute('UPDATE orders SET status = ? WHERE id = ?', (status, order_id))
    conn.commit()
    conn.close()

def validate_coupon(code, subtotal):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM coupons WHERE code = ? AND is_active = 1', (code,))
    coupon = c.fetchone()
    conn.close()
    
    if not coupon:
        return False, "Invalid or expired coupon"
        
    coupon = dict(coupon)
    if coupon['min_order_amount'] and subtotal < coupon['min_order_amount']:
        return False, f"Minimum order amount is ₹{coupon['min_order_amount']}"
        
    discount = 0
    if coupon['discount_percent']:
        discount = (subtotal * coupon['discount_percent']) / 100
        if coupon['max_discount'] and discount > coupon['max_discount']:
            discount = coupon['max_discount']
    elif coupon['fixed_discount']:
        discount = coupon['fixed_discount']
        
    return True, {"discount": discount, "code": code}

def get_dashboard_statistics():
    conn = get_connection()
    c = conn.cursor()
    
    c.execute('SELECT SUM(total) as revenue FROM orders')
    revenue = c.fetchone()['revenue'] or 0
    
    c.execute('SELECT COUNT(*) as total_orders FROM orders')
    total_orders = c.fetchone()['total_orders']
    
    c.execute('SELECT COUNT(*) as active_orders FROM orders WHERE status NOT IN ("Delivered", "Cancelled")')
    active_orders = c.fetchone()['active_orders']
    
    c.execute('SELECT COUNT(*) as total_customers FROM users WHERE role = "customer"')
    total_customers = c.fetchone()['total_customers']
    
    conn.close()
    
    return {
        "revenue": revenue,
        "total_orders": total_orders,
        "active_orders": active_orders,
        "total_customers": total_customers,
        "avg_order_value": revenue / total_orders if total_orders > 0 else 0
    }


def update_user(user_id, name, email):
    conn = get_connection()
    c = conn.cursor()
    c.execute('UPDATE users SET name = ?, email = ? WHERE id = ?', (name, email, user_id))
    conn.commit()
    conn.close()
    return get_user(user_id)

