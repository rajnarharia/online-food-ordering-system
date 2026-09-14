import os
import pandas as pd
import uuid
import hashlib
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')

SCHEMAS = {
    'users.csv': ['id', 'name', 'email', 'password_hash', 'role', 'loyalty_points', 'saved_addresses', 'referral_code'],
    'foods.csv': ['id', 'name', 'price', 'category', 'is_veg', 'rating', 'reviews', 'prep_time', 'popularity', 'description', 'calories', 'discount_percent', 'bestseller_badge', 'tags', 'nutrition_protein', 'nutrition_carbs', 'nutrition_fat', 'image_url', 'is_active'],
    'orders.csv': ['order_id', 'user_id', 'date', 'subtotal', 'tax', 'delivery_fee', 'discount', 'total', 'coupon_code', 'payment_method', 'status', 'delivery_instructions', 'address', 'estimated_delivery'],
    'order_items.csv': ['order_id', 'food_id', 'food_name', 'price', 'quantity', 'subtotal'],
    'wishlist.csv': ['user_id', 'food_id', 'added_at'],
    'addresses.csv': ['id', 'user_id', 'label', 'address', 'city', 'state', 'pincode', 'is_default'],
    'coupons.csv': ['code', 'discount_percent', 'minimum_order', 'maximum_discount', 'expiry_date', 'active'],
    'notifications.csv': ['id', 'user_id', 'message', 'notification_type', 'created_at', 'is_read']
}

def init_csv_files():
    os.makedirs(DATA_DIR, exist_ok=True)
    for filename, columns in SCHEMAS.items():
        filepath = os.path.join(DATA_DIR, filename)
        if not os.path.exists(filepath):
            pd.DataFrame(columns=columns).to_csv(filepath, index=False)

def get_filepath(filename):
    return os.path.join(DATA_DIR, filename)

def load_csv(filename):
    filepath = get_filepath(filename)
    if not os.path.exists(filepath):
        init_csv_files()
    try:
        df = pd.read_csv(filepath)
        return df
    except Exception:
        return pd.DataFrame(columns=SCHEMAS.get(filename, []))

def save_csv(filename, df):
    filepath = get_filepath(filename)
    df.to_csv(filepath, index=False)

def append_row(filename, row_dict):
    df = load_csv(filename)
    new_row = pd.DataFrame([row_dict])
    df = pd.concat([df, new_row], ignore_index=True)
    save_csv(filename, df)

def update_row(filename, match_col, match_val, update_dict):
    df = load_csv(filename)
    if match_col in df.columns:
        idx = df[df[match_col] == match_val].index
        if not idx.empty:
            for k, v in update_dict.items():
                df.loc[idx, k] = v
            save_csv(filename, df)
            return True
    return False

def delete_rows(filename, match_col, match_val):
    df = load_csv(filename)
    if match_col in df.columns:
        df = df[df[match_col] != match_val]
        save_csv(filename, df)

def generate_id():
    return str(uuid.uuid4())[:8]

def hash_password(password):
    return hashlib.sha256(str(password).encode()).hexdigest()
