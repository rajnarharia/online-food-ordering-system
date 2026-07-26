import streamlit as st
import json

def render_menu():
    st.markdown("<h2 class='hero-title' style='font-size: 2.5rem; margin-bottom: 24px;'>Craving something?</h2>", unsafe_allow_html=True)
    
    with open("data/foods.json", "r") as file:
        foods = json.load(file)
        
    # Filters
    c1, c2, c3 = st.columns(3)
    with c1:
        categories = ["All"] + list(set([f.get("category", "Other") for f in foods]))
        selected_category = st.selectbox("Category", categories)
    with c2:
        diet_filter = st.selectbox("Dietary", ["All", "Vegetarian", "Non-Vegetarian"])
    with c3:
        sort_by = st.selectbox("Sort", ["Recommended", "Price: Low to High", "Price: High to Low"])
        
    filtered_foods = foods
    
    if selected_category != "All":
        filtered_foods = [f for f in filtered_foods if f.get("category") == selected_category]
    if diet_filter == "Vegetarian":
        filtered_foods = [f for f in filtered_foods if f.get("is_veg", False)]
    elif diet_filter == "Non-Vegetarian":
        filtered_foods = [f for f in filtered_foods if not f.get("is_veg", True)]
        
    if sort_by == "Price: Low to High":
        filtered_foods.sort(key=lambda x: x["price"])
    elif sort_by == "Price: High to Low":
        filtered_foods.sort(key=lambda x: x["price"], reverse=True)
        
    st.write("<br>", unsafe_allow_html=True)
    
    if not filtered_foods:
        st.info("No items found matching your criteria.")
        return

    cols = st.columns(3, gap="large")
    
    for i, food in enumerate(filtered_foods):
        with cols[i % 3]:
            with st.container(border=True):
                st.image(food.get('image_url', 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?q=80&w=800'), use_container_width=True)
                
                # Tags formatted neatly
                tags = []
                if food.get('is_veg'): 
                    tags.append("<span class='pill-veg'>VEG</span>")
                if food.get('discount_percent', 0) > 0: 
                    tags.append(f"<span class='pill-discount'>{food['discount_percent']}% OFF</span>")
                
                if tags:
                    st.markdown("<div style='margin: 12px 0; display: flex; gap: 8px;'>" + "".join(tags) + "</div>", unsafe_allow_html=True)
                else:
                    st.write("<br>", unsafe_allow_html=True)
                
                # Title and description
                st.markdown(f"<p class='card-title'>{food['name']}</p>", unsafe_allow_html=True)
                st.markdown(f"<p class='card-meta'>{food.get('category', 'Cuisine')} • {food.get('calories', '0')} kcal</p>", unsafe_allow_html=True)
                
                # Price and rating
                price_col, rate_col = st.columns(2)
                price_col.markdown(f"<p class='price-tag'>₹{food['price']}</p>", unsafe_allow_html=True)
                rate_col.markdown(f"<p class='rating-tag'>★ {food.get('rating', 4.5)}</p>", unsafe_allow_html=True)
                
                st.write("")
                
                # Buttons
                btn1, btn2 = st.columns([1, 4])
                with btn1:
                    if st.button("♥", key=f"wish_{food['id']}"):
                        st.toast(f"Added {food['name']} to wishlist!")
                with btn2:
                    if st.button("Add to Cart", key=f"add_{food['id']}", type="primary", use_container_width=True):
                        st.session_state.cart.append(food)
                        st.toast(f"Added {food['name']} to cart!")
                        st.rerun()
