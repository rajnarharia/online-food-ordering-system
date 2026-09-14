import streamlit as st

# Set page config FIRST
st.set_page_config(
    page_title="Foodie",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ================= SESSION STATE INIT =================
if "cart" not in st.session_state:
    st.session_state.cart = []
if "current_view" not in st.session_state:
    st.session_state.current_view = "Home"
if "user" not in st.session_state:
    st.session_state.user = None
if "theme" not in st.session_state:
    st.session_state.theme = "Dark"
if "favorites" not in st.session_state:
    st.session_state.favorites = []
if "recently_viewed" not in st.session_state:
    st.session_state.recently_viewed = []

from utils.styles import inject_custom_css
from components.navbar import navbar
from views.home import render_home
from views.menu import render_menu
from views.cart_checkout import render_cart
from views.profile import render_profile
from views.admin_dashboard import render_admin
from views.static_pages import render_about
from views.ai_features import render_ai_features
from views.auth import render_login, render_register

# ================= GLOBAL STYLES =================
inject_custom_css()

# ================= NAVBAR =================
navbar()

# ================= ROUTING =================
view = st.session_state.current_view
user = st.session_state.user

with st.container():
    if view == "Login":
        render_login()
    elif view == "Register":
        render_register()
    elif view == "Home":
        render_home()
    elif view == "Menu":
        render_menu()
    elif view == "Cart":
        render_cart()
    elif view == "About":
        render_about()
    else:
        # Protected Routes
        if not user:
            st.warning("Please log in to access this page.")
            st.session_state.current_view = "Login"
            st.rerun()
        else:
            if view == "Profile" or view == "Orders":
                render_profile()
            elif view == "Admin":
                if user.get("role") == "admin":
                    render_admin()
                else:
                    st.error("Unauthorized access.")
                    st.session_state.current_view = "Home"
                    st.rerun()
            elif view == "AI":
                render_ai_features()
            else:
                render_home()

# ================= PROFESSIONAL FOOTER =================
st.write("<br><br><br>", unsafe_allow_html=True)
st.divider()

fc1, fc2, fc3, fc4 = st.columns([2, 1, 1, 1])

with fc1:
    accent_color = "#E23744" if st.session_state.theme == "Light" else "#FF5A5F"
    st.markdown(f"<h3 style='margin-top: 0px; margin-bottom: 8px; font-weight: 800; letter-spacing: -1px;'>Foodie<span style='color: {accent_color};'>.</span></h3>", unsafe_allow_html=True)
    st.markdown("<p class='card-meta'>Delivering happiness to your doorstep.<br>Fast, fresh, and always hot.</p>", unsafe_allow_html=True)
    st.markdown("<p class='card-meta' style='font-size: 0.8rem; margin-top: 24px;'>© 2026 Foodie Inc. All rights reserved.</p>", unsafe_allow_html=True)

with fc2:
    st.markdown("<p style='font-weight: 700; margin-bottom: 12px;'>Company</p>", unsafe_allow_html=True)
    st.markdown("<p class='card-meta' style='margin-bottom: 8px; cursor: pointer;'>About Us</p>", unsafe_allow_html=True)
    st.markdown("<p class='card-meta' style='margin-bottom: 8px; cursor: pointer;'>Careers</p>", unsafe_allow_html=True)
    st.markdown("<p class='card-meta' style='margin-bottom: 8px; cursor: pointer;'>Blog</p>", unsafe_allow_html=True)

with fc3:
    st.markdown("<p style='font-weight: 700; margin-bottom: 12px;'>Support</p>", unsafe_allow_html=True)
    st.markdown("<p class='card-meta' style='margin-bottom: 8px; cursor: pointer;'>Help Center</p>", unsafe_allow_html=True)
    st.markdown("<p class='card-meta' style='margin-bottom: 8px; cursor: pointer;'>Safety</p>", unsafe_allow_html=True)
    st.markdown("<p class='card-meta' style='margin-bottom: 8px; cursor: pointer;'>Terms of Service</p>", unsafe_allow_html=True)

with fc4:
    st.markdown("<p style='font-weight: 700; margin-bottom: 12px;'>Legal</p>", unsafe_allow_html=True)
    st.markdown("<p class='card-meta' style='margin-bottom: 8px; cursor: pointer;'>Privacy Policy</p>", unsafe_allow_html=True)
    st.markdown("<p class='card-meta' style='margin-bottom: 8px; cursor: pointer;'>Cookie Policy</p>", unsafe_allow_html=True)
    st.markdown("<p class='card-meta' style='margin-bottom: 8px; cursor: pointer;'>Compliance</p>", unsafe_allow_html=True)