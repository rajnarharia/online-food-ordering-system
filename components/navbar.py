import streamlit as st
from streamlit_option_menu import option_menu

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
    
    c1, c2, c3 = st.columns([1, 4, 2], vertical_alignment="center")
    
    with c1:
        st.markdown("<div style='font-size: 24px; font-weight: 800; letter-spacing: -1px;'>Foodie<span style='color: #FF5A5F;'>.</span></div>", unsafe_allow_html=True)
        
    with c2:
        cart_count = sum(item['quantity'] for item in st.session_state.cart)
        user = st.session_state.user
        
        options = ["Home", "Menu"]
        if user:
            if user.get("role") == "admin":
                options.append("Admin")
            else:
                options.append("AI")
        
        current = st.session_state.current_view if st.session_state.current_view in options else "Home"
        if st.session_state.current_view not in options and st.session_state.current_view in ["Cart", "Profile", "Login", "Register", "About", "Orders"]:
            # If current view is not in options, don't break option_menu
            current = options[0]
            
        selected_view = option_menu(
            menu_title=None,
            options=options,
            default_index=options.index(current) if current in options else 0,
            orientation="horizontal",
            styles={
                "container": {"padding": "0!important", "background-color": "transparent"},
                "nav-link": {
                    "font-size": "14px", 
                    "text-align": "center", 
                    "margin": "0px 12px", 
                    "color": "#9CA3AF",
                    "font-weight": "500",
                    "border-radius": "0px",
                },
                "nav-link-selected": {
                    "background-color": "transparent",
                    "color": "#FFFFFF",
                    "font-weight": "600",
                    "border-bottom": "2px solid #FF5A5F"
                },
            }
        )
        
    with c3:
        if user:
            i1, i2, i3 = st.columns(3)
            with i1:
                btn_label = f"🛒 {cart_count}" if cart_count > 0 else "🛒"
                if st.button(btn_label, key="nav_cart", use_container_width=True):
                    st.session_state.current_view = "Cart"
                    st.rerun()
            with i2:
                if st.button("👤", key="nav_profile", use_container_width=True):
                    st.session_state.current_view = "Profile"
                    st.rerun()
            with i3:
                if st.button("Logout", key="nav_logout", use_container_width=True):
                    st.session_state.user = None
                    st.session_state.cart = []
                    st.session_state.current_view = "Login"
                    st.rerun()
        else:
            i1, i2 = st.columns(2)
            with i1:
                if st.button("Login", key="nav_login_btn", use_container_width=True):
                    st.session_state.current_view = "Login"
                    st.rerun()
            with i2:
                if st.button("Register", key="nav_reg_btn", use_container_width=True):
                    st.session_state.current_view = "Register"
                    st.rerun()
                
    if st.session_state.current_view != selected_view and selected_view in options:
        if st.session_state.current_view not in ["Cart", "Profile", "Login", "Register", "About", "Orders"]:
            st.session_state.current_view = selected_view
            st.rerun()
