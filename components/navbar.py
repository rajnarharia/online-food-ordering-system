import streamlit as st
from streamlit_option_menu import option_menu

def navbar():
    # Subtle top spacing
    st.write("<br>", unsafe_allow_html=True)
    
    # Use 3 columns for Logo, Menu, and Theme Toggle
    col1, col2, col3 = st.columns([1.5, 4.5, 0.5])
    
    with col1:
        # Luxury Logo styling matching the Playfair Display Midnight Gourmet theme
        if st.session_state.theme == "Light":
            accent_color = "#F43F5E"
            text_color = "#0F172A"
        else:
            accent_color = "#FF4B2B"
            text_color = "#F8FAFC"
            
        st.markdown(
            f"""
            <div style='margin-top: 2px;'>
                <h2 style="font-family: 'Playfair Display', serif; margin: 0; font-weight: 800; font-size: 2.2rem; color: {text_color}; letter-spacing: -0.02em;">
                    Foodie<span style='color: {accent_color};'>.</span>
                </h2>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
    with col2:
        cart_count = len(st.session_state.cart)
        cart_label = f"Cart ({cart_count})" if cart_count > 0 else "Cart"
        
        options = ["Home", "Menu", "AI Assistant", cart_label, "Orders", "Profile", "Admin"]
        
        current = st.session_state.current_view
        default_idx = options.index(current) if current in options else (options.index(cart_label) if current == "Cart" else 0)
        
        # Premium Colors for the Navigation Menu
        if st.session_state.theme == "Light":
            nav_text = "#475569"
            nav_bg_active = "rgba(244, 63, 94, 0.1)"
            nav_text_active = "#F43F5E"
        else:
            nav_text = "#94A3B8"
            nav_bg_active = "rgba(255, 75, 43, 0.15)"
            nav_text_active = "#FF4B2B"
        
        selected_view = option_menu(
            menu_title=None,
            options=options,
            default_index=default_idx,
            orientation="horizontal",
            styles={
                "container": {
                    "padding": "0!important", 
                    "background-color": "transparent",
                    "margin-top": "0px"
                },
                "nav-link": {
                    "font-family": "'Manrope', sans-serif",
                    "font-size": "14px", 
                    "text-align": "center", 
                    "margin": "0px 2px", 
                    "color": nav_text,
                    "font-weight": "600",
                    "border-radius": "100px", # Pill shaped navigation items
                    "text-transform": "uppercase",
                    "letter-spacing": "0.05em",
                    "padding": "12px 16px",
                },
                "nav-link-selected": {
                    "background-color": nav_bg_active,
                    "color": nav_text_active,
                    "font-weight": "800",
                    "border": f"1px solid rgba(255, 75, 43, 0.3)" if st.session_state.theme == "Dark" else f"1px solid rgba(244, 63, 94, 0.3)"
                },
            }
        )
        
    with col3:
        # Elegant Theme Toggle
        icon = "🌙" if st.session_state.theme == "Light" else "☀️"
        if st.button(icon, key="theme_toggle", help="Toggle Theme"):
            st.session_state.theme = "Dark" if st.session_state.theme == "Light" else "Light"
            st.rerun()
        
    # Replaced default chunky divider with elegant custom gradient divider
    st.markdown(
        """
        <div style="height: 1px; background: linear-gradient(90deg, transparent, rgba(150, 150, 150, 0.2), transparent); margin: 1.5rem 0 2rem 0;"></div>
        """, 
        unsafe_allow_html=True
    )
        
    target_view = selected_view
    if selected_view.startswith("Cart"):
        target_view = "Cart"
        
    if st.session_state.current_view != target_view:
        st.session_state.current_view = target_view
        st.rerun()
