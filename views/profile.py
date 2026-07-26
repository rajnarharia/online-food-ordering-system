import streamlit as st
import json

def render_profile():
    st.markdown("<h2 class='hero-title' style='font-size: 2.5rem; margin-bottom: 24px;'>Account</h2>", unsafe_allow_html=True)
    
    with open("data/users.json", "r") as f:
        users = json.load(f)
    user = users[0]
    
    pc1, pc2 = st.columns([1, 2], gap="large")
    
    with pc1:
        with st.container(border=True):
            st.markdown(f"<p class='card-title'>{user['name']}</p>", unsafe_allow_html=True)
            st.markdown(f"<p class='card-meta'>{user['email']}</p>", unsafe_allow_html=True)
            
            st.markdown("<p class='stat-label' style='margin-top: 24px;'>Reward Points</p>", unsafe_allow_html=True)
            st.markdown(f"<p class='price-tag' style='color: #E23744;'>{user.get('loyalty_points', 0)}</p>", unsafe_allow_html=True)
            
            st.write("<br>", unsafe_allow_html=True)
            st.markdown(
                """
                <div style="width: 100%; background-color: rgba(0,0,0,0.05); height: 8px; border-radius: 4px; overflow: hidden; margin-bottom: 8px;">
                    <div style="width: 70%; background: linear-gradient(90deg, #E23744, #FF5A5F); height: 100%;"></div>
                </div>
                <span class='card-meta' style='font-size: 11px;'>70% to Gold Tier</span>
                """, 
                unsafe_allow_html=True
            )
            
            st.write("<br>", unsafe_allow_html=True)
            st.button("Edit Settings", use_container_width=True)
            
    with pc2:
        st.markdown("<p class='card-title' style='margin-bottom: 16px;'>Recent Orders</p>", unsafe_allow_html=True)
        
        with open("data/orders.json", "r") as file:
            orders = json.load(file)
            
        if not orders:
            st.markdown("<p class='card-meta'>No recent orders.</p>", unsafe_allow_html=True)
        else:
            for order in reversed(orders[-5:]): # Show last 5
                with st.container(border=True):
                    oc1, oc2 = st.columns([3, 1])
                    with oc1:
                        items_str = ', '.join([item['name'] for item in order.get('items', [])])
                        st.markdown(f"<p class='card-title' style='font-size: 1rem; margin:0;'>{items_str}</p>", unsafe_allow_html=True)
                        st.markdown(f"<span class='card-meta'>{order.get('date', '')[:10]}</span>", unsafe_allow_html=True)
                    with oc2:
                        st.markdown(f"<p class='price-tag' style='font-size: 1.1rem; float: right; margin:0;'>₹{order.get('total')}</p>", unsafe_allow_html=True)
