import streamlit as st
from utils.helpers import get_all_products, filter_products, add_to_cart

def show_products_page():
    # Header
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.title("🌿 GreenChoice")
    with col2:
        st.write(f"👤 {st.session_state.user['name']}")
    with col3:
        cart_count = len(st.session_state.cart)
        if st.button(f"🛒 Cart ({cart_count})"):
            st.session_state.page = 'cart'
            st.rerun()
    
    if st.button("🚪 Logout", key="logout_btn"):
        st.session_state.user = None
        st.session_state.cart = []
        st.session_state.page = 'login'
        st.rerun()
    
    st.divider()
    
    # Search and Filters
    st.session_state.search_term = st.text_input("🔍 Search products", 
                                                   value=st.session_state.search_term)
    
    with st.expander("🔧 Filters"):
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.filters['vegan'] = st.checkbox("Vegan", 
                                                             value=st.session_state.filters['vegan'])
            st.session_state.filters['carbon_neutral'] = st.checkbox("Carbon Neutral", 
                                                                      value=st.session_state.filters['carbon_neutral'])
        with col2:
            st.session_state.filters['fair_trade'] = st.checkbox("Fair Trade", 
                                                                  value=st.session_state.filters['fair_trade'])
            st.session_state.filters['organic'] = st.checkbox("Organic", 
                                                               value=st.session_state.filters['organic'])
        
        st.session_state.filters['min_rating'] = st.slider("Minimum Sustainability Rating", 
                                                            0, 100, 
                                                            st.session_state.filters['min_rating'], 10)
    
    # Get and filter products
    products = get_all_products()
    filtered_products = filter_products(products, st.session_state.filters, st.session_state.search_term)
    
    st.subheader(f"Sustainable Products ({len(filtered_products)} found)")
    
    # Display products in grid
    cols_per_row = 3
    for i in range(0, len(filtered_products), cols_per_row):
        cols = st.columns(cols_per_row)
        for j, col in enumerate(cols):
            if i + j < len(filtered_products):
                product = filtered_products[i + j]
                with col:
                    show_product_card(product)

def show_product_card(product):
    """Display a product card"""
    st.image(product['image'], use_container_width=True)
    st.markdown(f"**{product['name']}**")
    st.write(f"${product['price']}")
    
    # Sustainability rating
    rating = product['sustainability_rating']
    if rating >= 90:
        rating_class = "rating-high"
    elif rating >= 75:
        rating_class = "rating-medium"
    else:
        rating_class = "rating-low"
    
    st.markdown(f"<span class='rating-badge {rating_class}'>{rating}/100</span>", 
                unsafe_allow_html=True)
    
    # Attributes
    attrs = product['attributes']
    if attrs['vegan']:
        st.markdown("<span class='attribute-badge badge-vegan'>Vegan</span>", 
                    unsafe_allow_html=True)
    if attrs['carbon_neutral']:
        st.markdown("<span class='attribute-badge badge-carbon'>Carbon Neutral</span>", 
                    unsafe_allow_html=True)
    if attrs['fair_trade']:
        st.markdown("<span class='attribute-badge badge-fair'>Fair Trade</span>", 
                    unsafe_allow_html=True)
    if attrs['organic']:
        st.markdown("<span class='attribute-badge badge-organic'>Organic</span>", 
                    unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("View", key=f"view_{product['product_id']}"):
            st.session_state.selected_product = product
            st.session_state.page = 'product_detail'
            st.rerun()
    with col2:
        if st.button("Add to Cart", key=f"add_{product['product_id']}"):
            add_to_cart(product)
            st.success("Added!")
            st.rerun()