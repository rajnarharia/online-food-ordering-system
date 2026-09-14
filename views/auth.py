import streamlit as st
from database.db import authenticate_user, create_user

def render_login():
    st.markdown("<h2 class='section-title' style='text-align: center;'>Welcome Back</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.container(border=True):
            st.markdown("<h3 class='card-title'>Login</h3>", unsafe_allow_html=True)
            email = st.text_input("Email", value="admin@foodie.com", key="login_email")
            password = st.text_input("Password", type="password", value="admin123", key="login_password")
            
            if st.button("Sign In", type="primary", use_container_width=True):
                if email and password:
                    user = authenticate_user(email, password)
                    if user:
                        st.session_state.user = user
                        st.session_state.current_view = "Home"
                        st.rerun()
                    else:
                        st.error("Invalid email or password")
                else:
                    st.error("Please enter email and password")
                    
            st.markdown("<p style='text-align: center; margin-top: 16px;'>Don't have an account?</p>", unsafe_allow_html=True)
            if st.button("Create Account", use_container_width=True):
                st.session_state.current_view = "Register"
                st.rerun()

def render_register():
    st.markdown("<h2 class='section-title' style='text-align: center;'>Create an Account</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.container(border=True):
            st.markdown("<h3 class='card-title'>Register</h3>", unsafe_allow_html=True)
            name = st.text_input("Full Name", key="reg_name")
            email = st.text_input("Email", key="reg_email")
            password = st.text_input("Password", type="password", key="reg_password")
            confirm_password = st.text_input("Confirm Password", type="password", key="reg_confirm")
            
            if st.button("Sign Up", type="primary", use_container_width=True):
                if name and email and password and confirm_password:
                    if password != confirm_password:
                        st.error("Passwords do not match")
                    else:
                        user = create_user(name, email, password)
                        if user:
                            st.success("Account created successfully! Please log in.")
                            st.session_state.current_view = "Login"
                            st.rerun()
                        else:
                            st.error("Email already exists")
                else:
                    st.error("Please fill all fields")
                    
            st.markdown("<p style='text-align: center; margin-top: 16px;'>Already have an account?</p>", unsafe_allow_html=True)
            if st.button("Log In", use_container_width=True):
                st.session_state.current_view = "Login"
                st.rerun()
