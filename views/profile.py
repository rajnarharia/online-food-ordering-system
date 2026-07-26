import streamlit as st
import json
from datetime import datetime

def render_profile():
    st.markdown("<h1 class='section-title' style='margin-bottom: 32px;'>Your Profile</h1>", unsafe_allow_html=True)
    
    # Premium Profile Dashboard Layout
    c1, c2 = st.columns([1, 2.5], gap="large")
    
    # Grab real user data
    user = st.session_state.user or {}
    name = user.get("name", "Guest User")
    email = user.get("email", "guest@example.com")
    points = user.get("loyalty_points", 0)
    initial = name[0] if name else "G"
    
    with c1:
        # User Card
        with st.container(border=True):
            st.markdown(
                f"""
                <div style='text-align: center; padding: 16px 0;'>
                    <div style='width: 96px; height: 96px; border-radius: 50%; background: linear-gradient(135deg, #FF5A5F, #E04E53); margin: 0 auto 16px auto; display: flex; align-items: center; justify-content: center; font-size: 36px; font-weight: 700; color: #FFF; box-shadow: 0 10px 25px rgba(255, 90, 95, 0.4);'>
                        {initial}
                    </div>
                    <h3 class='card-title' style='margin: 0 0 4px 0;'>{name}</h3>
                    <p class='small-text' style='margin: 0;'>{email}</p>
                </div>
                """, 
                unsafe_allow_html=True
            )
            
            st.write("<br>", unsafe_allow_html=True)
            
            # Reward Points
            st.markdown(
                f"""
                <div style='background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255,255,255,0.05); border-radius: 12px; padding: 16px; margin-bottom: 16px;'>
                    <div style='display: flex; justify-content: space-between; align-items: center;'>
                        <span class='small-text' style='font-weight: 600; text-transform: uppercase;'>Reward Points</span>
                        <span style='color: #FACC15; font-size: 16px;'>★</span>
                    </div>
                    <p style='font-size: 28px; font-weight: 700; margin: 8px 0 0 0; color: #FFF;'>{points:,}</p>
                </div>
                """, 
                unsafe_allow_html=True
            )
            
            # Nav Links (Simulation -> Replaced with functional Edit Profile)
            with st.expander("✏️ Edit Profile"):
                new_name = st.text_input("Name", value=name)
                new_email = st.text_input("Email", value=email)
                if st.button("Save Changes", type="primary"):
                    if st.session_state.user:
                        try:
                            with open("data/users.json", "r") as f:
                                users = json.load(f)
                            for u in users:
                                if u['id'] == st.session_state.user['id']:
                                    u['name'] = new_name
                                    u['email'] = new_email
                                    st.session_state.user['name'] = new_name
                                    st.session_state.user['email'] = new_email
                                    break
                            with open("data/users.json", "w") as f:
                                json.dump(users, f, indent=4)
                            st.toast("Profile updated successfully!", icon="✅")
                            st.rerun()
                        except Exception as e:
                            st.error("Failed to update profile.")
                            
            st.markdown("<p class='body-text' style='cursor: pointer; padding: 12px; border-radius: 8px; transition: all 0.2s; font-weight: 500;'>📍 Saved Addresses</p>", unsafe_allow_html=True)
            st.markdown("<p class='body-text' style='cursor: pointer; padding: 12px; border-radius: 8px; transition: all 0.2s; font-weight: 500;'>⚙️ Settings</p>", unsafe_allow_html=True)
            
    with c2:
        st.markdown("<h3 class='card-title' style='font-size: 20px; margin-bottom: 24px;'>Recent Orders</h3>", unsafe_allow_html=True)
        
        # Real Order Timeline
        try:
            with open("data/orders.json", "r") as f:
                all_orders = json.load(f)
                # Sort by date descending and grab last 5
                all_orders.sort(key=lambda x: x.get('date', ''), reverse=True)
                recent_orders = all_orders[:5]
        except Exception:
            recent_orders = []
            
        if not recent_orders:
            st.markdown("<p class='body-text'>No recent orders found.</p>", unsafe_allow_html=True)
        
        for order in recent_orders:
            with st.container(border=True):
                col_a, col_b, col_c = st.columns([2, 1, 1], vertical_alignment="center")
                
                # Format date nicely if possible
                date_str = order.get('date', '')
                try:
                    dt = datetime.fromisoformat(date_str)
                    display_date = dt.strftime("%b %d, %I:%M %p")
                except:
                    display_date = date_str
                    
                items_str = ", ".join([item['name'] for item in order.get('items', [])])
                
                with col_a:
                    st.markdown(f"<p style='font-weight: 700; color: #FFF; margin: 0 0 4px 0;'>{order['id']}</p>", unsafe_allow_html=True)
                    st.markdown(f"<p class='small-text' style='margin: 0;'>{items_str}</p>", unsafe_allow_html=True)
                    
                with col_b:
                    st.markdown(f"<p class='small-text' style='margin: 0;'>{display_date}</p>", unsafe_allow_html=True)
                    status = order.get('status', 'Unknown')
                    status_color = "#22C55E" if status in ["Delivered", "Preparing"] else "#EF4444"
                    st.markdown(f"<p style='font-size: 12px; font-weight: 600; color: {status_color}; margin: 4px 0 0 0;'>{status}</p>", unsafe_allow_html=True)
                    
                with col_c:
                    st.markdown(f"<p style='font-size: 18px; font-weight: 700; color: #FFF; margin: 0 0 8px 0; text-align: right;'>${order.get('total', 0):.2f}</p>", unsafe_allow_html=True)
                    if st.button("Reorder", key=f"reorder_{order['id']}", use_container_width=True):
                        # Reorder logic: actually pull from data/foods.json to get full item objects
                        try:
                            with open("data/foods.json", "r") as f:
                                db_foods = {item['id']: item for item in json.load(f)}
                            
                            added_count = 0
                            for item in order.get('items', []):
                                if item['id'] in db_foods:
                                    st.session_state.cart.append(db_foods[item['id']])
                                    added_count += 1
                                    
                            st.toast(f"{added_count} items from {order['id']} added to cart!", icon="✅")
                            st.rerun()
                        except Exception as e:
                            st.error("Failed to reorder items.")
