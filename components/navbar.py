import streamlit as st

def navbar():
    # Adding floating glass navbar styles dynamically for this component
    st.markdown(
        """
        <style>
        .floating-nav-container {
            position: fixed;
            top: 16px;
            left: 50%;
            transform: translateX(-50%);
            width: 95%;
            max-width: 1200px;
            background: rgba(17, 24, 39, 0.7); /* Card BG with transparency */
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 100px;
            padding: 12px 24px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            z-index: 99999;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
            transition: all 0.3s ease;
        }
        
        .nav-logo {
            font-size: 20px;
            font-weight: 700;
            color: #FFFFFF;
            letter-spacing: -0.02em;
            cursor: pointer;
        }
        .nav-logo span { color: #FF5A5F; }
        
        .nav-links {
            display: flex;
            gap: 32px;
            align-items: center;
        }
        .nav-link {
            font-size: 14px;
            font-weight: 500;
            color: #9CA3AF;
            text-decoration: none;
            cursor: pointer;
            transition: color 0.2s ease;
            position: relative;
        }
        .nav-link:hover { color: #FFFFFF; }
        .nav-link.active {
            color: #FFFFFF;
            font-weight: 600;
        }
        .nav-link.active::after {
            content: '';
            position: absolute;
            bottom: -6px;
            left: 0;
            right: 0;
            height: 2px;
            background: #FF5A5F;
            border-radius: 2px;
        }
        
        .nav-actions {
            display: flex;
            gap: 16px;
            align-items: center;
        }
        .nav-icon {
            color: #9CA3AF;
            font-size: 18px;
            cursor: pointer;
            transition: color 0.2s ease;
        }
        .nav-icon:hover { color: #FFFFFF; }
        
        .cart-badge {
            background: #FF5A5F;
            color: white;
            font-size: 10px;
            font-weight: 700;
            padding: 2px 6px;
            border-radius: 10px;
            position: absolute;
            top: -8px;
            right: -10px;
        }
        
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
    
    # State routing logic via invisible streamlit buttons to maintain state mapping
    # Since we use raw HTML for the visual navbar, we need a way to trigger Streamlit's reruns.
    # We will render invisible Streamlit buttons over the HTML using absolute positioning tricks,
    # OR we just rely on a Streamlit native columns hack styled to look like the HTML.
    # Given Streamlit's constraints, it's safer to use `st.columns` and heavily style them to look like the floating nav.
    
    st.markdown("<div class='floating-nav-container'></div>", unsafe_allow_html=True)
    
    # To make Streamlit elements stick inside the floating container, we use a custom hack.
    # Actually, wrapping st.columns in a container and assigning a class via markdown is the most reliable way in native Streamlit.
    
    # We create a container, but streamlit assigns generic classes. 
    # Let's use `streamlit_option_menu` for the links but completely strip its styles, and put it in columns.
    from streamlit_option_menu import option_menu
    
    c1, c2, c3 = st.columns([1, 3, 1], vertical_alignment="center")
    
    with c1:
        st.markdown("<div style='font-size: 20px; font-weight: 700; letter-spacing: -0.02em;'>Foodie<span style='color: #FF5A5F;'>.</span></div>", unsafe_allow_html=True)
        
    with c2:
        cart_count = len(st.session_state.cart)
        options = ["Home", "Menu", "Orders", "AI", "About"]
        current = st.session_state.current_view if st.session_state.current_view in options else "Home"
        
        selected_view = option_menu(
            menu_title=None,
            options=options,
            default_index=options.index(current),
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
        i1, i2, i3, i4 = st.columns(4)
        with i1:
            st.button("🔍", key="nav_search", help="Search")
        with i2:
            # Cart icon with indicator
            btn_label = f"🛒 {cart_count}" if cart_count > 0 else "🛒"
            if st.button(btn_label, key="nav_cart"):
                st.session_state.current_view = "Cart"
                st.rerun()
        with i3:
            st.button("🔔", key="nav_notif")
        with i4:
            if st.button("👤", key="nav_profile"):
                st.session_state.current_view = "Profile"
                st.rerun()
                
    if st.session_state.current_view != selected_view and selected_view in options:
        st.session_state.current_view = selected_view
        st.rerun()
