import streamlit as st 
from utils.helpers import add_to_cart

def show_product_detail_page():
    product = st.session_state.selected_product
    
    if st.button("← Back to Products"):
        st.session_state.page = 'products'
        st.rerun()
    
    st.title(product['name'])
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.image(product['image'], use_container_width=True)
    
    with col2:
        st.subheader(f"${product['price']}")
        st.write(f"**Category:** {product['category']}")
        
        # Sustainability Rating
        rating = product['sustainability_rating']
        st.metric("Sustainability Rating", f"{rating}/100")
        st.progress(rating / 100)
        
        # Attributes
        st.subheader("Eco-Friendly Attributes")
        attrs = product['attributes']
        
        st.write("✅ Vegan" if attrs['vegan'] else "")
        st.write("✅ Carbon Neutral" if attrs['carbon_neutral'] else "")
        st.write("✅ Fair Trade" if attrs['fair_trade'] else "")
        st.write("✅ Organic" if attrs['organic'] else "")
        st.write("✅ Recycled Materials" if attrs['recycled_materials'] else "")
        
        if st.button("🛒 Add to Cart", use_container_width=True):
            add_to_cart(product)
            st.success("Added to cart!")
            st.rerun()
    
    st.divider()
    st.subheader("Product Description")
    st.write(product['description'])