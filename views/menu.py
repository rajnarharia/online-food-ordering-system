import streamlit as st
import json

def render_menu():
    st.markdown("<h1 class='section-title' style='margin-bottom: 8px;'>Explore Menu</h1>", unsafe_allow_html=True)
    st.markdown("<p class='body-text' style='margin-bottom: 32px;'>Discover our hand-crafted selection of premium dishes.</p>", unsafe_allow_html=True)
    
    # State init for new features
    if "recently_viewed" not in st.session_state:
        st.session_state.recently_viewed = []
    if "favorites" not in st.session_state:
        st.session_state.favorites = []
        
    try:
        with open("data/foods.json", "r") as file:
            foods = json.load(file)
    except:
        foods = []
        
    # Search System (Real Instant Filtering & Smart Suggestions simulation)
    search_col, filter_col = st.columns([2, 1])
    with search_col:
        search_query = st.text_input("Search dishes, ingredients, or categories...", placeholder="e.g. Spicy Chicken Burger")
    with filter_col:
        diet_filter = st.selectbox("Dietary Preference", ["All", "Vegetarian", "Non-Vegetarian"])
        
    st.write("<br>", unsafe_allow_html=True)
    
    # Filtering logic
    filtered_foods = foods
    if search_query:
        q = search_query.lower()
        filtered_foods = [f for f in foods if q in f['name'].lower() or q in f.get('category', '').lower()]
    if diet_filter == "Vegetarian":
        filtered_foods = [f for f in filtered_foods if f.get('is_veg', False)]
    elif diet_filter == "Non-Vegetarian":
        filtered_foods = [f for f in filtered_foods if not f.get('is_veg', True)]
        
    if not filtered_foods:
        st.markdown(
            """
            <div style='text-align: center; padding: 64px 0;'>
                <h3 class='card-title' style='color: #9CA3AF;'>No matches found</h3>
                <p class='body-text'>Try adjusting your search or filters.</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
        return

    # Render Grid
    cols = st.columns(3, gap="large")
    
    for i, food in enumerate(filtered_foods):
        with cols[i % 3]:
            with st.container(border=True):
                # Image with overlay and badges
                is_fav = food['id'] in st.session_state.favorites
                fav_color = "#FF5A5F" if is_fav else "rgba(255,255,255,0.8)"
                
                badges = []
                if food.get('is_veg'):
                    badges.append("<span class='badge badge-success' style='position: absolute; top: 12px; left: 12px; z-index: 10;'>VEG</span>")
                if food.get('discount_percent', 0) > 0:
                    badges.append(f"<span class='badge badge-accent' style='position: absolute; top: 12px; right: 12px; z-index: 10;'>{food['discount_percent']}% OFF</span>")
                
                badges_html = "".join(badges)
                
                # Uber-Eats Style High-End Card
                st.markdown(
                    f"""
                    <div style='position: relative; height: 220px; border-radius: 16px; overflow: hidden; margin-bottom: 16px;'>
                        {badges_html}
                        <img src='{food.get('image_url', 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?q=80&w=800')}' style='width: 100%; height: 100%; object-fit: cover;' />
                        <div style='position: absolute; bottom: 0; left: 0; right: 0; height: 50%; background: linear-gradient(to top, rgba(17,24,39,1), transparent); pointer-events: none;'></div>
                        <div style='position: absolute; bottom: 12px; left: 12px; display: flex; align-items: center; gap: 8px;'>
                            <span style='background: rgba(255,255,255,0.1); backdrop-filter: blur(8px); padding: 4px 8px; border-radius: 8px; font-size: 12px; font-weight: 600; color: #FFF;'><span style='color: #FACC15;'>★</span> {food.get('rating', 4.5)}</span>
                            <span style='background: rgba(255,255,255,0.1); backdrop-filter: blur(8px); padding: 4px 8px; border-radius: 8px; font-size: 12px; font-weight: 600; color: #FFF;'>25 min</span>
                        </div>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
                
                # Title and Desc
                st.markdown(f"<h3 class='card-title' style='margin: 0 0 4px 0;'>{food['name']}</h3>", unsafe_allow_html=True)
                st.markdown(f"<p class='small-text' style='margin: 0 0 16px 0;'>{food.get('category', 'Cuisine')} • {food.get('calories', '0')} kcal</p>", unsafe_allow_html=True)
                
                # Price and Buttons
                p_col, b1, b2 = st.columns([2, 1, 1.5])
                with p_col:
                    st.markdown(f"<p style='font-size: 20px; font-weight: 700; color: #FFFFFF; margin: 0; display: flex; height: 100%; align-items: center;'>${food['price']}</p>", unsafe_allow_html=True)
                with b1:
                    fav_icon = "❤️" if is_fav else "🤍"
                    if st.button(fav_icon, key=f"fav_{food['id']}", help="Add to favorites"):
                        if is_fav:
                            st.session_state.favorites.remove(food['id'])
                        else:
                            st.session_state.favorites.append(food['id'])
                            
                        # Persist to JSON
                        if st.session_state.user:
                            try:
                                with open("data/users.json", "r") as f:
                                    users = json.load(f)
                                for u in users:
                                    if u['id'] == st.session_state.user['id']:
                                        u['wishlist_items'] = st.session_state.favorites
                                        break
                                with open("data/users.json", "w") as f:
                                    json.dump(users, f, indent=4)
                            except Exception:
                                pass
                                
                        st.rerun()
                with b2:
                    if st.button("Add", key=f"add_{food['id']}", type="primary"):
                        st.session_state.cart.append(food)
                        if food['id'] not in [f['id'] for f in st.session_state.recently_viewed]:
                            st.session_state.recently_viewed.append(food)
                            if len(st.session_state.recently_viewed) > 4:
                                st.session_state.recently_viewed.pop(0)
                        st.toast(f"Added {food['name']} to cart!", icon="✅")
                        st.rerun()

    # Recently Viewed Section (New Feature)
    if st.session_state.recently_viewed:
        st.write("<br><br><br>", unsafe_allow_html=True)
        st.markdown("<h2 class='section-title' style='margin-bottom: 24px; font-size: 24px;'>Recently Viewed</h2>", unsafe_allow_html=True)
        r_cols = st.columns(4)
        for i, r_food in enumerate(st.session_state.recently_viewed):
            with r_cols[i % 4]:
                with st.container(border=True):
                    st.markdown(f"<p class='card-title' style='font-size: 16px; margin: 0;'>{r_food['name']}</p>", unsafe_allow_html=True)
                    st.markdown(f"<p class='small-text' style='margin: 4px 0 0 0;'>${r_food['price']}</p>", unsafe_allow_html=True)
