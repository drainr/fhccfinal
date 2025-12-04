import streamlit as st
from utils.helpers import update_quantity, remove_from_cart, get_cart_total, get_cart_avg_rating

def show_cart_page():
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("🛒 Shopping Cart")
    with col2:
        if st.button("← Continue Shopping"):
            st.session_state.page = 'products'
            st.rerun()
    
    if not st.session_state.cart:
        st.info("Your cart is empty. Start shopping for sustainable products!")
        return
    
    # Display cart items
    for item in st.session_state.cart:
        col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
        
        with col1:
            st.image(item['image'], width=100)
        
        with col2:
            st.write(f"**{item['name']}**")
            st.write(f"${item['price']}")
            st.markdown(f"<span class='rating-badge rating-high'>{item['sustainability_rating']}/100</span>", 
                        unsafe_allow_html=True)
        
        with col3:
            quantity = st.number_input("Qty", 
                                       min_value=0, 
                                       value=item['quantity'], 
                                       key=f"qty_{item['product_id']}")
            if quantity != item['quantity']:
                update_quantity(item['product_id'], quantity)
                st.rerun()
        
        with col4:
            if st.button("🗑️", key=f"remove_{item['product_id']}"):
                remove_from_cart(item['product_id'])
                st.rerun()
        
        st.divider()
    
    # Order Summary
    st.subheader("Order Summary")
    total = get_cart_total()
    avg_rating = get_cart_avg_rating()
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total", f"${total:.2f}")
    with col2:
        st.metric("Avg Sustainability", f"{avg_rating}/100")
    
    if st.button("Proceed to Checkout", type="primary", use_container_width=True):
        st.session_state.page = 'checkout'
        st.rerun()