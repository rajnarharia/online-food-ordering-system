import streamlit as st

def navbar():
    st.markdown(
        """
        <style>
        .nav-avatar {
            width: 32px;
            height: 32px;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.1);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 14px;
            color: #FFFFFF;
            cursor: pointer;
            border: 1px solid rgba(255,255,255,0.2);
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # We use a container to act as the navbar
    c1, c2, c3, c4, c5, c6, c7, c8 = st.columns([2, 1, 1, 1, 1, 1.5, 1, 1])
    
    with c1:
        st.markdown("<div style='font-size: 24px; font-weight: 800; letter-spacing: -1px; cursor: default;'>Foodie<span style='color: #E11D48;'>.</span></div>", unsafe_allow_html=True)
        
    user = st.session_state.user
    
    def nav_btn(label, view_name, col):
        with col:
            is_active = st.session_state.current_view == view_name
            btn_type = "primary" if is_active else "secondary"
            if st.button(label, key=f"nav_{view_name}", use_container_width=True, type=btn_type):
                st.session_state.current_view = view_name
                st.rerun()

    nav_btn("Home", "Home", c2)
    nav_btn("Menu", "Menu", c3)
    
    if user:
        if user.get("role") == "admin":
            nav_btn("Admin", "Admin", c4)
        else:
            nav_btn("AI", "AI", c4)
            
        nav_btn("Profile", "Profile", c5)
        
        cart_count = sum(item['quantity'] for item in st.session_state.cart)
        nav_btn(f"🛒 {cart_count}", "Cart", c6)
        
        with c7:
            if st.button("Logout", key="nav_logout", use_container_width=True):
                st.session_state.user = None
                st.session_state.cart = []
                st.session_state.favorites = []
                st.session_state.current_view = "Login"
                st.rerun()
    else:
        nav_btn("Cart (0)", "Cart", c5)
        nav_btn("Login", "Login", c6)
        nav_btn("Register", "Register", c7)
        
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
