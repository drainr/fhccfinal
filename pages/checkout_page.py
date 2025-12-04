import streamlit as st
from utils.helpers import get_cart_total, get_cart_avg_rating, save_order

def show_checkout_page():
    if st.button("← Back to Cart"):
        st.session_state.page = 'cart'
        st.rerun()
    
    st.title("Checkout")
    
    with st.form("checkout_form"):
        st.subheader("Shipping Information")
        col1, col2 = st.columns(2)
        with col1:
            full_name = st.text_input("Full Name", value=st.session_state.user['name'])
            email = st.text_input("Email", value=st.session_state.user['email'])
        with col2:
            address = st.text_input("Address")
            city = st.text_input("City")
            zip_code = st.text_input("ZIP Code", max_chars=5)
        
        st.subheader("Payment Information")
        col1, col2 = st.columns(2)
        with col1:
            card_number = st.text_input("Card Number", placeholder="1234 5678 9012 3456", max_chars=16)
            expiry = st.text_input("Expiry Date", placeholder="MM/YY")
        with col2:
            cvv = st.text_input("CVV", placeholder="123", type="password", max_chars=4)
        
        st.divider()
        st.subheader("Order Summary")
        total = get_cart_total()
        avg_rating = get_cart_avg_rating()
        
        for item in st.session_state.cart:
            st.write(f"{item['name']} x{item['quantity']} - ${item['price'] * item['quantity']:.2f}")
        
        st.write(f"**Total: ${total:.2f}**")
        st.write(f"**Avg Sustainability Rating: {avg_rating}/100**")
        
        submit = st.form_submit_button("Complete Order", type="primary", use_container_width=True)
        
        if submit:
            # Validate all required fields are filled
            if not (full_name.strip() and email.strip() and address.strip() and 
                    city.strip() and zip_code.strip() and card_number.strip() and 
                    expiry.strip() and cvv.strip()):
                st.error("Please fill in all fields before completing your order.")
            else:
                save_order()
                st.session_state.cart = []
                st.success("🎉 Order completed successfully!")
                st.balloons()
                st.info(f"Your sustainability impact: {avg_rating}/100")
                st.write("Thank you for shopping sustainably with GreenChoice!")
    
    # Continue Shopping button outside the form
    if st.session_state.cart == [] and st.session_state.get('order_completed', False):
        if st.button("Continue Shopping"):
            st.session_state.page = 'products'
            st.rerun()