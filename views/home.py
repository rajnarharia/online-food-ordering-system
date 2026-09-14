import streamlit as st
from utils.data_store import get_foods

def render_home():
    # Hero Section
    c1, c2 = st.columns([1.1, 1], gap="large")
    
    with c1:
        st.write("<br><br>", unsafe_allow_html=True)
        st.markdown("<div class='hero-title'>Craving it? <br><span style='color: #E11D48;'>Get it.</span></div>", unsafe_allow_html=True)
        st.markdown(
            "<div class='body-text' style='margin-bottom: 32px;'>The fastest way to get your favorite meals delivered fresh and piping hot. Zero hassle, total satisfaction.</div>",
            unsafe_allow_html=True
        )
        
        b1, b2 = st.columns([1, 1])
        with b1:
            if st.button("Order Now", type="primary", use_container_width=True):
                st.session_state.current_view = "Menu"
                st.rerun()
        with b2:
            if st.button("Explore Menu", use_container_width=True):
                st.session_state.current_view = "Menu"
                st.rerun()
                
        st.write("<br><br>", unsafe_allow_html=True)
        
        # Trust Indicators
        m1, m2, m3 = st.columns(3)
        with m1:
            st.markdown("<p class='small-text' style='text-transform: uppercase; font-weight: 600; letter-spacing: 0.05em;'>Delivery Rating</p><p style='font-size: 32px; font-weight: 700; color: #FFFFFF; margin: 0;'>4.9 <span style='color: #FACC15; font-size: 24px;'>⭐</span></p>", unsafe_allow_html=True)
        with m2:
            st.markdown("<p class='small-text' style='text-transform: uppercase; font-weight: 600; letter-spacing: 0.05em;'>Active Users</p><p style='font-size: 32px; font-weight: 700; color: #FFFFFF; margin: 0;'>50k<span style='color: #E11D48;'>+</span></p>", unsafe_allow_html=True)
        with m3:
            st.markdown("<p class='small-text' style='text-transform: uppercase; font-weight: 600; letter-spacing: 0.05em;'>Avg Time</p><p style='font-size: 32px; font-weight: 700; color: #FFFFFF; margin: 0;'>24<span style='color: #E11D48; font-size: 24px;'>m</span></p>", unsafe_allow_html=True)
        
    with c2:
        st.write("<br>", unsafe_allow_html=True)
        st.markdown(
            """
            <div style="position: relative; border-radius: 24px; overflow: hidden; box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);">
                <img src="https://images.unsplash.com/photo-1504674900247-0877df9cc836?q=80&w=1000" style="width: 100%; height: auto; border-radius: 24px; filter: brightness(0.9);" />
                <div style="position: absolute; bottom: 24px; left: 24px; background: rgba(17, 24, 39, 0.8); backdrop-filter: blur(12px); padding: 12px 20px; border-radius: 16px; border: 1px solid rgba(255,255,255,0.1); display: flex; align-items: center; gap: 12px;">
                    <div style="background: #22C55E; border-radius: 50%; width: 12px; height: 12px; box-shadow: 0 0 10px #22C55E;"></div>
                    <span style="font-weight: 600; font-size: 14px; color: #FFFFFF;">Live Delivery Available</span>
                </div>
            </div>
            """, 
            unsafe_allow_html=True
        )

    st.write("<br><br><br><br>", unsafe_allow_html=True)
    
    # Trending Section
    st.markdown("<h2 class='section-title'>Trending Today</h2>", unsafe_allow_html=True)
    
    foods = get_foods(sort_by='popularity')
    trending = foods[:4] if len(foods) >= 4 else foods
    
    if trending:
        cols = st.columns(4)
        for i, food in enumerate(trending):
            with cols[i % 4]:
                with st.container():
                    st.markdown(f"<div style='height: 180px; overflow: hidden; border-radius: 16px; margin-bottom: 16px;'><img src='{food.get('image_url', 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?q=80&w=800')}' style='width: 100%; height: 100%; object-fit: cover;' /></div>", unsafe_allow_html=True)
                    st.markdown(f"<h3 class='card-title' style='margin: 0 0 4px 0;'>{food['name']}</h3>", unsafe_allow_html=True)
                    st.markdown(f"<p class='small-text' style='margin: 0 0 16px 0;'>{food.get('category', 'Category')} • {food.get('calories', '0')} kcal</p>", unsafe_allow_html=True)
                    
                    price_col, btn_col = st.columns([1, 1])
                    with price_col:
                        st.markdown(f"<p style='font-size: 18px; font-weight: 700; margin: 0; color: #FFFFFF;'>₹{food['price']}</p>", unsafe_allow_html=True)
                    with btn_col:
                        if st.button("Add", key=f"trend_{food['id']}", use_container_width=True):
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
        st.write("<br><br>", unsafe_allow_html=True)
        st.markdown("<h2 class='section-title'>Recently Viewed</h2>", unsafe_allow_html=True)
        recent_ids = st.session_state.recently_viewed[:4]
        from utils.data_store import get_food
        
        recent_foods = []
        for fid in recent_ids:
            rf = get_food(fid)
            if rf: recent_foods.append(rf)
            
        if recent_foods:
            r_cols = st.columns(4)
            for i, food in enumerate(recent_foods):
                with r_cols[i % 4]:
                    with st.container():
                        st.markdown(f"<h3 class='card-title' style='margin: 0 0 4px 0; font-size: 16px;'>{food['name']}</h3>", unsafe_allow_html=True)
                        st.markdown(f"<p style='font-size: 14px; font-weight: 700; margin: 0; color: #E11D48;'>₹{food['price']}</p>", unsafe_allow_html=True)
                        
    st.write("<br><br><br>", unsafe_allow_html=True)
