import json
import os
import sqlite3
from schema import init_db
from db import create_user, get_connection

def seed_database():
    # Re-initialize DB
    db_path = os.path.join(os.path.dirname(__file__), '..', 'foodie.db')
    if os.path.exists(db_path):
        os.remove(db_path)
    init_db()
    
    # Create Admin
    create_user("Admin", "admin@foodie.com", "admin123", role="admin")
    
    # Seed Foods
    foods_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'foods.json')
    if os.path.exists(foods_path):
        with open(foods_path, 'r', encoding='utf-8') as f:
            foods = json.load(f)
            
        conn = get_connection()
        c = conn.cursor()
        for food in foods:
            tags = ",".join(food.get('tags', []))
            nut_p = food.get('nutrition_info', {}).get('protein', '')
            nut_c = food.get('nutrition_info', {}).get('carbs', '')
            nut_f = food.get('nutrition_info', {}).get('fat', '')
            
            c.execute('''
            INSERT INTO foods (name, price, category, is_veg, rating, reviews, prep_time, popularity, 
                               description, calories, discount_percent, bestseller_badge, tags, 
                               nutrition_protein, nutrition_carbs, nutrition_fat, image_url)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                food['name'], food['price'], food['category'], food['is_veg'], food['rating'], 
                food['reviews'], food['prep_time'], food['popularity'], food['description'], 
                food['calories'], food['discount_percent'], food['bestseller_badge'], tags, 
                nut_p, nut_c, nut_f, food['image_url']
            ))
        conn.commit()
        conn.close()
        print(f"Seeded {len(foods)} foods.")
        
    # Seed Coupons
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
    INSERT INTO coupons (code, discount_percent, min_order_amount, is_active)
    VALUES (?, ?, ?, ?)
    ''', ('SAAS10', 10, 500, 1))
    conn.commit()
    conn.close()
    
    print("Database seeding completed.")

if __name__ == "__main__":
    seed_database()
