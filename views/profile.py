import streamlit as st
from datetime import datetime
from utils.data_store import get_user_orders, update_user, get_food

def render_profile():
    st.markdown("<h1 class='section-title' style='margin-bottom: 32px;'>Your Profile</h1>", unsafe_allow_html=True)
    
    user = st.session_state.user
    if not user:
        st.warning("Please log in to view your profile.")
        return
        
    c1, c2 = st.columns([1, 2.5], gap="large")
    
    name = user.get("name", "Guest")
    email = user.get("email", "")
    points = user.get("loyalty_points", 0)
    initial = name[0].upper() if name else "G"
    
    with c1:
        with st.container():
            st.markdown(
                f"""
                <div style='text-align: center; padding: 16px 0;'>
                    <div style='width: 96px; height: 96px; border-radius: 50%; background: linear-gradient(135deg, #E11D48, #BE123C); margin: 0 auto 16px auto; display: flex; align-items: center; justify-content: center; font-size: 36px; font-weight: 700; color: #FFF; box-shadow: 0 10px 25px rgba(225, 29, 72, 0.4);'>
                        {initial}
                    </div>
                    <h3 class='card-title' style='margin: 0 0 4px 0;'>{name}</h3>
                    <p class='small-text' style='margin: 0;'>{email}</p>
                </div>
                """, 
                unsafe_allow_html=True
            )
            
            st.write("<br>", unsafe_allow_html=True)
            
            st.markdown(
                f"""
                <div style='background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255,255,255,0.05); border-radius: 12px; padding: 16px; margin-bottom: 16px;'>
                    <div style='display: flex; justify-content: space-between; align-items: center;'>
                        <span class='small-text' style='font-weight: 600; text-transform: uppercase;'>Reward Points</span>
                        <span style='color: #FACC15; font-size: 16px;'>🏆</span>
                    </div>
                    <p style='font-size: 28px; font-weight: 700; margin: 8px 0 0 0; color: #FFF;'>{points:,}</p>
                </div>
                """, 
                unsafe_allow_html=True
            )
            
            with st.expander("✏️ Edit Profile"):
                new_name = st.text_input("Name", value=name)
                new_email = st.text_input("Email", value=email)
                if st.button("Save Changes", type="primary", use_container_width=True):
                    try:
                        updated = update_user(user['id'], new_name, new_email)
                        if updated:
                            st.session_state.user = updated
                            st.success("Profile updated successfully!")
                            st.rerun()
                        else:
                            st.error("Failed to update profile.")
                    except Exception as e:
                        st.error("Email may already be in use.")
                            
            if st.button("Logout", use_container_width=True):
                st.session_state.user = None
                st.session_state.cart = []
                st.session_state.favorites = []
                st.session_state.current_view = "Login"
                st.rerun()
            
    with c2:
        st.markdown("<h3 class='card-title' style='font-size: 20px; margin-bottom: 24px;'>Recent Orders</h3>", unsafe_allow_html=True)
        
        recent_orders = get_user_orders(user['id'])
            
        if not recent_orders:
            st.markdown("<p class='body-text'>No recent orders found.</p>", unsafe_allow_html=True)
        
        for order in recent_orders:
            with st.container():
                col_a, col_b, col_c = st.columns([2, 1, 1])
                
                date_str = order.get('date', '')
                try:
                    dt = datetime.fromisoformat(date_str)
                    display_date = dt.strftime("%b %d, %I:%M %p")
                except:
                    display_date = date_str
                    
                items_str = ", ".join([f"{item['quantity']}x {item['name']}" for item in order.get('items', [])])
                
                with col_a:
                    st.markdown(f"<p style='font-weight: 700; color: #FFF; margin: 0 0 4px 0;'>{order['id']}</p>", unsafe_allow_html=True)
                    st.markdown(f"<p class='small-text' style='margin: 0;'>{items_str}</p>", unsafe_allow_html=True)
                    
                with col_b:
                    st.markdown(f"<p class='small-text' style='margin: 0;'>{display_date}</p>", unsafe_allow_html=True)
                    status = order.get('status', 'Unknown')
                    status_color = "#22C55E" if status in ["Delivered", "Order Placed", "Confirmed"] else "#FACC15" if status in ["Preparing", "Out for Delivery"] else "#EF4444"
                    st.markdown(f"<p style='font-size: 12px; font-weight: 600; color: {status_color}; margin: 4px 0 0 0;'>{status}</p>", unsafe_allow_html=True)
                    
                with col_c:
                    st.markdown(f"<p style='font-size: 18px; font-weight: 700; color: #FFF; margin: 0 0 8px 0; text-align: right;'>₹{order.get('total', 0):.2f}</p>", unsafe_allow_html=True)
                    if st.button("Reorder", key=f"reorder_{order['id']}", use_container_width=True):
                        added_count = 0
                        for item in order.get('items', []):
                            food_db = get_food(item['food_id'])
                            if food_db:
                                # Check if already in cart
                                existing = next((c for c in st.session_state.cart if c['id'] == food_db['id']), None)
                                if existing:
                                    existing['quantity'] += item['quantity']
                                else:
                                    f_to_add = food_db.copy()
                                    f_to_add['quantity'] = item['quantity']
                                    st.session_state.cart.append(f_to_add)
                                added_count += 1
                                
                        st.toast(f"{added_count} items added to cart!", icon="🛒")
                        st.session_state.current_view = "Cart"
                        st.rerun()
