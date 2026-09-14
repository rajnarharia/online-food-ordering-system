import streamlit as st
from database.db import get_foods, add_to_wishlist, remove_from_wishlist, get_wishlist, get_food

def render_menu():
    st.markdown("<h1 class='section-title' style='margin-bottom: 8px;'>Explore Menu</h1>", unsafe_allow_html=True)
    st.markdown("<p class='body-text' style='margin-bottom: 32px;'>Discover our hand-crafted selection of premium dishes.</p>", unsafe_allow_html=True)
    
    user = st.session_state.user
    if user and "favorites" not in st.session_state:
        st.session_state.favorites = get_wishlist(user['id'])
    elif not user:
        st.session_state.favorites = []
        
    if "recently_viewed" not in st.session_state:
        st.session_state.recently_viewed = []
        
    search_col, filter_col, sort_col = st.columns([2, 1, 1])
    with search_col:
        search_query = st.text_input("Search dishes, ingredients, or categories...", placeholder="e.g. Spicy Chicken Burger")
    with filter_col:
        diet_filter = st.selectbox("Dietary Preference", ["All", "Vegetarian", "Non-Vegetarian"])
    with sort_col:
        sort_by = st.selectbox("Sort By", ["Relevance", "Price Low to High", "Price High to Low", "Rating", "Popularity"])
        
    st.write("<br>", unsafe_allow_html=True)
    
    sort_map = {
        "Relevance": None,
        "Price Low to High": "price_asc",
        "Price High to Low": "price_desc",
        "Rating": "rating",
        "Popularity": "popularity"
    }
    
    is_veg = None
    if diet_filter == "Vegetarian":
        is_veg = True
    elif diet_filter == "Non-Vegetarian":
        is_veg = False
        
    filtered_foods = get_foods(
        search=search_query if search_query else None,
        is_veg=is_veg,
        sort_by=sort_map[sort_by]
    )
        
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
                is_fav = food['id'] in st.session_state.favorites
                
                badges = []
                if food.get('is_veg'):
                    badges.append("<span class='badge badge-success' style='position: absolute; top: 12px; left: 12px; z-index: 10;'>VEG</span>")
                if food.get('discount_percent', 0) > 0:
                    badges.append(f"<span class='badge badge-accent' style='position: absolute; top: 12px; right: 12px; z-index: 10;'>{food['discount_percent']}% OFF</span>")
                
                badges_html = "".join(badges)
                
                st.markdown(
                    f"""
                    <div style='position: relative; height: 220px; border-radius: 16px; overflow: hidden; margin-bottom: 16px;'>
                        {badges_html}
                        <img src='{food.get('image_url', 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?q=80&w=800')}' style='width: 100%; height: 100%; object-fit: cover;' />
                        <div style='position: absolute; bottom: 0; left: 0; right: 0; height: 50%; background: linear-gradient(to top, rgba(17,24,39,1), transparent); pointer-events: none;'></div>
                        <div style='position: absolute; bottom: 12px; left: 12px; display: flex; align-items: center; gap: 8px;'>
                            <span style='background: rgba(255,255,255,0.1); backdrop-filter: blur(8px); padding: 4px 8px; border-radius: 8px; font-size: 12px; font-weight: 600; color: #FFF;'><span style='color: #FACC15;'>⭐</span> {food.get('rating', 4.5)}</span>
                            <span style='background: rgba(255,255,255,0.1); backdrop-filter: blur(8px); padding: 4px 8px; border-radius: 8px; font-size: 12px; font-weight: 600; color: #FFF;'>{food.get('prep_time', 20)} min</span>
                        </div>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
                
                st.markdown(f"<h3 class='card-title' style='margin: 0 0 4px 0;'>{food['name']}</h3>", unsafe_allow_html=True)
                st.markdown(f"<p class='small-text' style='margin: 0 0 16px 0;'>{food.get('category', 'Cuisine')} • {food.get('calories', '0')} kcal</p>", unsafe_allow_html=True)
                
                p_col, b1, b2 = st.columns([2, 1, 1.5])
                with p_col:
                    st.markdown(f"<p style='font-size: 20px; font-weight: 700; color: #FFFFFF; margin: 0; display: flex; height: 100%; align-items: center;'>₹{food['price']}</p>", unsafe_allow_html=True)
                with b1:
                    fav_icon = "❤️" if is_fav else "🤍"
                    if st.button(fav_icon, key=f"fav_{food['id']}", help="Add to wishlist"):
                        if not user:
                            st.warning("Please log in to use wishlist.")
                        else:
                            if is_fav:
                                st.session_state.favorites.remove(food['id'])
                                remove_from_wishlist(user['id'], food['id'])
                            else:
                                st.session_state.favorites.append(food['id'])
                                add_to_wishlist(user['id'], food['id'])
                            st.rerun()
                with b2:
                    if st.button("Add", key=f"add_{food['id']}", type="primary", use_container_width=True):
                        # Track recently viewed
                        if food['id'] not in st.session_state.recently_viewed:
                            st.session_state.recently_viewed.insert(0, food['id'])
                            if len(st.session_state.recently_viewed) > 4:
                                st.session_state.recently_viewed = st.session_state.recently_viewed[:4]
                                
                        # Handle quantity mapping
                        existing = next((item for item in st.session_state.cart if item['id'] == food['id']), None)
                        if existing:
                            existing['quantity'] += 1
                        else:
                            food_to_add = food.copy()
                            food_to_add['quantity'] = 1
                            st.session_state.cart.append(food_to_add)
                            
                        st.toast(f"Added {food['name']} to cart!")
                        st.rerun()

    # Recently Viewed Section
    if st.session_state.recently_viewed:
        st.write("<br><br><br>", unsafe_allow_html=True)
        st.markdown("<h2 class='section-title' style='margin-bottom: 24px; font-size: 24px;'>Recently Viewed</h2>", unsafe_allow_html=True)
        r_cols = st.columns(4)
        for i, fid in enumerate(st.session_state.recently_viewed):
            r_food = get_food(fid)
            if not r_food: continue
            with r_cols[i % 4]:
                with st.container(border=True):
                    st.markdown(f"<p class='card-title' style='font-size: 16px; margin: 0;'>{r_food['name']}</p>", unsafe_allow_html=True)
                    st.markdown(f"<p class='small-text' style='margin: 4px 0 0 0;'>₹{r_food['price']}</p>", unsafe_allow_html=True)
