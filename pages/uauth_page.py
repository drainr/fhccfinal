import streamlit as st
from utils.helpers import signup_user, login_user

def show_auth_page():
    st.markdown("<h1 style='text-align: center; color: #2d6a4f;'>🌿 GreenChoice</h1>", 
                unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #666;'>Shop sustainably, live responsibly</p>", 
                unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    with tab1:
        st.subheader("Welcome Back")
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login")
            
            if submit:
                user = login_user(email, password)
                if user:
                    st.session_state.user = user
                    # restore user's cart if present
                    st.session_state.cart = user.get('cart', []) if user else []
                    st.session_state.page = 'products'
                    st.rerun()
                else:
                    st.error("Invalid credentials!")
    
    with tab2:
        st.subheader("Create Account")
        with st.form("signup_form"):
            name = st.text_input("Full Name")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Sign Up")
            
            if submit:
                success, message = signup_user(email, password, name)
                if success:
                    st.success(message)
                    user = login_user(email, password)
                    st.session_state.user = user
                    st.session_state.cart = user.get('cart', []) if user else []
                    st.session_state.page = 'products'
                    st.rerun()
                else:
                    st.error(message)