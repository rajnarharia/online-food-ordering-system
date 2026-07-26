import streamlit as st

def render_profile():
    st.markdown("<h1 class='section-title' style='margin-bottom: 32px;'>Your Profile</h1>", unsafe_allow_html=True)
    
    # Premium Profile Dashboard Layout
    c1, c2 = st.columns([1, 2.5], gap="large")
    
    with c1:
        # User Card
        with st.container(border=True):
            st.markdown(
                """
                <div style='text-align: center; padding: 16px 0;'>
                    <div style='width: 96px; height: 96px; border-radius: 50%; background: linear-gradient(135deg, #FF5A5F, #E04E53); margin: 0 auto 16px auto; display: flex; align-items: center; justify-content: center; font-size: 36px; font-weight: 700; color: #FFF; box-shadow: 0 10px 25px rgba(255, 90, 95, 0.4);'>
                        J
                    </div>
                    <h3 class='card-title' style='margin: 0 0 4px 0;'>John Doe</h3>
                    <p class='small-text' style='margin: 0;'>john.doe@example.com</p>
                </div>
                """, 
                unsafe_allow_html=True
            )
            
            st.write("<br>", unsafe_allow_html=True)
            
            # Reward Points
            st.markdown(
                """
                <div style='background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255,255,255,0.05); border-radius: 12px; padding: 16px; margin-bottom: 16px;'>
                    <div style='display: flex; justify-content: space-between; align-items: center;'>
                        <span class='small-text' style='font-weight: 600; text-transform: uppercase;'>Reward Points</span>
                        <span style='color: #FACC15; font-size: 16px;'>★</span>
                    </div>
                    <p style='font-size: 28px; font-weight: 700; margin: 8px 0 0 0; color: #FFF;'>2,450</p>
                </div>
                """, 
                unsafe_allow_html=True
            )
            
            # Nav Links (Simulation)
            st.markdown("<p class='body-text' style='cursor: pointer; padding: 12px; border-radius: 8px; transition: all 0.2s; font-weight: 500;'>📍 Saved Addresses</p>", unsafe_allow_html=True)
            st.markdown("<p class='body-text' style='cursor: pointer; padding: 12px; border-radius: 8px; transition: all 0.2s; font-weight: 500;'>❤️ Wishlist</p>", unsafe_allow_html=True)
            st.markdown("<p class='body-text' style='cursor: pointer; padding: 12px; border-radius: 8px; transition: all 0.2s; font-weight: 500;'>⚙️ Settings</p>", unsafe_allow_html=True)
            
    with c2:
        st.markdown("<h3 class='card-title' style='font-size: 20px; margin-bottom: 24px;'>Recent Orders</h3>", unsafe_allow_html=True)
        
        # Order Timeline
        orders = [
            {"id": "#ORD-8821", "date": "Today, 1:45 PM", "status": "Delivered", "items": "Spicy Chicken Burger, Fries", "total": "$18.50"},
            {"id": "#ORD-8742", "date": "Oct 24, 8:12 PM", "status": "Delivered", "items": "Margherita Pizza", "total": "$24.00"},
            {"id": "#ORD-8519", "date": "Oct 18, 12:30 PM", "status": "Cancelled", "items": "Sushi Platter", "total": "$45.00"}
        ]
        
        for order in orders:
            with st.container(border=True):
                col_a, col_b, col_c = st.columns([2, 1, 1], vertical_alignment="center")
                
                with col_a:
                    st.markdown(f"<p style='font-weight: 700; color: #FFF; margin: 0 0 4px 0;'>{order['id']}</p>", unsafe_allow_html=True)
                    st.markdown(f"<p class='small-text' style='margin: 0;'>{order['items']}</p>", unsafe_allow_html=True)
                    
                with col_b:
                    st.markdown(f"<p class='small-text' style='margin: 0;'>{order['date']}</p>", unsafe_allow_html=True)
                    status_color = "#22C55E" if order['status'] == "Delivered" else "#EF4444"
                    st.markdown(f"<p style='font-size: 12px; font-weight: 600; color: {status_color}; margin: 4px 0 0 0;'>{order['status']}</p>", unsafe_allow_html=True)
                    
                with col_c:
                    st.markdown(f"<p style='font-size: 18px; font-weight: 700; color: #FFF; margin: 0 0 8px 0; text-align: right;'>{order['total']}</p>", unsafe_allow_html=True)
                    if st.button("Reorder", key=f"reorder_{order['id']}", use_container_width=True):
                        st.toast(f"Items from {order['id']} added to cart!", icon="✅")
