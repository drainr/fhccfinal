import streamlit as st
from utils.styling import load_css
from db import init_session_state, init_sample_products
from pages.uauth_page import show_auth_page
from pages.products_page import show_products_page
from pages.product_detail_page import show_product_detail_page
from pages.cart_page import show_cart_page
from pages.checkout_page import show_checkout_page

def main():
    st.set_page_config(page_title="GreenChoice", page_icon="🌿", layout="wide")
    load_css()
    init_session_state()
    init_sample_products()
    
    # Route to appropriate page
    if st.session_state.page == 'login':
        show_auth_page()
    elif st.session_state.page == 'products':
        show_products_page()
    elif st.session_state.page == 'product_detail':
        show_product_detail_page()
    elif st.session_state.page == 'cart':
        show_cart_page()
    elif st.session_state.page == 'checkout':
        show_checkout_page()

if __name__ == "__main__":
    main()