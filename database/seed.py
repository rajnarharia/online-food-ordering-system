import json
import os
import sqlite3
from database.schema import init_db
from database.db import create_user, get_connection

def seed_database():
    # Clear existing data safely
    init_db()
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM users")
    c.execute("DELETE FROM foods")
    c.execute("DELETE FROM coupons")
    conn.commit()
    conn.close()
    
    # Create Admin
    create_user("Admin", "admin@foodie.com", "admin123", role="admin")
    
    # Seed Foods
    foods_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'foods.json')
    if os.path.exists(foods_path):
        with open(foods_path, 'r', encoding='utf-8') as f:
            foods = json.load(f)
    else:
        foods = [
            {
                "name": "Classic Cheeseburger", "price": 199.0, "category": "Fast Food", "is_veg": False, 
                "rating": 4.5, "reviews": 120, "prep_time": "15-20 min", "popularity": 95, 
                "description": "Juicy beef patty with melted cheese.", "calories": 650, 
                "discount_percent": 0, "bestseller_badge": True, "tags": ["burger", "beef"], 
                "nutrition_info": {"protein": "25g", "carbs": "40g", "fat": "30g"},
                "image_url": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=500&q=80"
            },
            {
                "name": "Margherita Pizza", "price": 299.0, "category": "Italian", "is_veg": True, 
                "rating": 4.8, "reviews": 200, "prep_time": "20-25 min", "popularity": 98, 
                "description": "Classic pizza with fresh mozzarella and basil.", "calories": 800, 
                "discount_percent": 10, "bestseller_badge": True, "tags": ["pizza", "veg"], 
                "nutrition_info": {"protein": "30g", "carbs": "90g", "fat": "20g"},
                "image_url": "https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=500&q=80"
            }
        ]
        
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
