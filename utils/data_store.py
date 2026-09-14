from utils.csv_handler import load_csv, save_csv, append_row, update_row, delete_rows, generate_id, hash_password, init_csv_files
import pandas as pd
from datetime import datetime

# --- USERS ---
def create_user(name, email, password, role='customer'):
    df = load_csv('users.csv')
    if email in df['email'].values:
        return None
    
    user_id = generate_id()
    user = {
        'id': user_id, 'name': name, 'email': email,
        'password_hash': hash_password(password),
        'role': role, 'loyalty_points': 0, 'saved_addresses': '', 'referral_code': ''
    }
    append_row('users.csv', user)
    return get_user(user_id)

def authenticate_user(email, password):
    df = load_csv('users.csv')
    hashed_pw = hash_password(password)
    user = df[(df['email'] == email) & (df['password_hash'] == hashed_pw)]
    if not user.empty:
        return user.iloc[0].to_dict()
    return None

def get_user(user_id):
    df = load_csv('users.csv')
    user = df[df['id'] == str(user_id)]
    if not user.empty:
        return user.iloc[0].to_dict()
    return None

def update_user(user_id, name, email):
    df = load_csv('users.csv')
    if not df[(df['email'] == email) & (df['id'] != str(user_id))].empty:
        raise Exception("Email already exists")
    
    success = update_row('users.csv', 'id', str(user_id), {'name': name, 'email': email})
    if success:
        return get_user(user_id)
    return None

# --- FOODS ---
def get_foods(category=None, is_veg=None, min_price=None, max_price=None, search=None, sort_by=None):
    df = load_csv('foods.csv')
    if df.empty:
        return []
        
    df = df[df['is_active'].astype(str).str.lower().isin(['true', '1', 'yes'])]
    
    if is_veg is not None:
        if is_veg:
            df = df[df['is_veg'].astype(str).str.lower().isin(['true', '1', 'yes'])]
        else:
            df = df[df['is_veg'].astype(str).str.lower().isin(['false', '0', 'no'])]
            
    if search:
        search = search.lower()
        df = df[df['name'].astype(str).str.lower().str.contains(search, na=False) | df['category'].astype(str).str.lower().str.contains(search, na=False)]
        
    if min_price is not None:
        df = df[pd.to_numeric(df['price'], errors='coerce') >= min_price]
    if max_price is not None:
        df = df[pd.to_numeric(df['price'], errors='coerce') <= max_price]
        
    if sort_by:
        if sort_by == 'price_asc':
            df = df.sort_values(by='price', ascending=True)
        elif sort_by == 'price_desc':
            df = df.sort_values(by='price', ascending=False)
        elif sort_by in df.columns:
            df = df.sort_values(by=sort_by, ascending=False)
            
    return df.to_dict('records')

def get_food(food_id):
    df = load_csv('foods.csv')
    food = df[df['id'] == str(food_id)]
    if not food.empty:
        return food.iloc[0].to_dict()
    return None

def toggle_food_active(food_id, is_active):
    update_row('foods.csv', 'id', str(food_id), {'is_active': is_active})

def add_food(food_dict):
    if 'id' not in food_dict:
        food_dict['id'] = generate_id()
    append_row('foods.csv', food_dict)

# --- ORDERS ---
def create_order(user_id, subtotal, tax, delivery_fee, discount, total, items, coupon_code=""):
    order_id = "ORD-" + generate_id().upper()
    order = {
        'order_id': order_id,
        'user_id': user_id,
        'date': datetime.now().isoformat(),
        'subtotal': subtotal,
        'tax': tax,
        'delivery_fee': delivery_fee,
        'discount': discount,
        'total': total,
        'coupon_code': coupon_code,
        'payment_method': 'Online',
        'status': 'Order Placed',
        'delivery_instructions': '',
        'address': '',
        'estimated_delivery': ''
    }
    append_row('orders.csv', order)
    
    items_df = []
    for item in items:
        items_df.append({
            'order_id': order_id,
            'food_id': item['id'],
            'food_name': item['name'],
            'price': item['price'],
            'quantity': item['quantity'],
            'subtotal': item['price'] * item['quantity']
        })
    
    if items_df:
        o_df = load_csv('order_items.csv')
        new_items = pd.DataFrame(items_df)
        o_df = pd.concat([o_df, new_items], ignore_index=True)
        save_csv('order_items.csv', o_df)
        
    create_notification(user_id, f"Order {order_id} has been placed successfully.", "order")
    return order_id

def get_all_orders():
    orders_df = load_csv('orders.csv')
    return orders_df.to_dict('records')

def get_user_orders(user_id):
    orders_df = load_csv('orders.csv')
    if orders_df.empty:
        return []
    user_orders = orders_df[orders_df['user_id'] == str(user_id)].sort_values(by='date', ascending=False).to_dict('records')
    
    items_df = load_csv('order_items.csv')
    for order in user_orders:
        if not items_df.empty:
            order_items = items_df[items_df['order_id'] == order['order_id']].to_dict('records')
            order['items'] = [{'food_id': i['food_id'], 'name': i['food_name'], 'price': i['price'], 'quantity': i['quantity']} for i in order_items]
        else:
            order['items'] = []
        order['id'] = order['order_id']
    return user_orders

def update_order_status(order_id, status):
    update_row('orders.csv', 'order_id', str(order_id), {'status': status})
    df = load_csv('orders.csv')
    order = df[df['order_id'] == str(order_id)]
    if not order.empty:
        user_id = order.iloc[0]['user_id']
        create_notification(user_id, f"Order {order_id} status updated to: {status}", "status_update")

# --- COUPONS ---
def validate_coupon(code, subtotal):
    df = load_csv('coupons.csv')
    coupon = df[(df['code'] == code) & (df['active'].astype(str).str.lower().isin(['true', '1', 'yes']))]
    if coupon.empty:
        return False, "Invalid or expired coupon"
    
    c = coupon.iloc[0].to_dict()
    min_ord = pd.to_numeric(c.get('minimum_order', 0), errors='coerce')
    if min_ord and subtotal < min_ord:
        return False, f"Minimum order amount is ₹{min_ord}"
    return True, c

# --- WISHLIST ---
def get_wishlist(user_id):
    df = load_csv('wishlist.csv')
    if df.empty:
        return []
    favs = df[df['user_id'] == str(user_id)]['food_id'].tolist()
    return [str(f) for f in favs]

def add_to_wishlist(user_id, food_id):
    df = load_csv('wishlist.csv')
    if df.empty or df[(df['user_id'] == str(user_id)) & (df['food_id'] == str(food_id))].empty:
        append_row('wishlist.csv', {'user_id': str(user_id), 'food_id': str(food_id), 'added_at': datetime.now().isoformat()})

def remove_from_wishlist(user_id, food_id):
    df = load_csv('wishlist.csv')
    if not df.empty:
        df = df[~((df['user_id'] == str(user_id)) & (df['food_id'] == str(food_id)))]
        save_csv('wishlist.csv', df)

# --- NOTIFICATIONS ---
def create_notification(user_id, message, type="general"):
    append_row('notifications.csv', {
        'id': generate_id(),
        'user_id': str(user_id),
        'message': message,
        'notification_type': type,
        'created_at': datetime.now().isoformat(),
        'is_read': False
    })
