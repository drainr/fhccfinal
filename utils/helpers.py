import streamlit as st
import hashlib 
import datetime
from db import users_collection, products_collection, orders_collection

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def signup_user(email, password, name):
    """Create a new user account"""
    if users_collection.find_one({"email": email}):
        return False, "User already exists!"
    
    user = {
        "email": email,
        "password": hash_password(password),
        "name": name,
                "created_at": datetime.datetime.now(),
                "cart": []
    }
    users_collection.insert_one(user)
    return True, "Account created successfully!"

def login_user(email, password):
    """Authenticate user"""
    user = users_collection.find_one({
        "email": email,
        "password": hash_password(password)
    })
    return user

def get_all_products():
    """Retrieve all products from database"""
    return list(products_collection.find({}, {'_id': 0}))

def filter_products(products, filters, search_term):
    """Filter products based on criteria"""
    filtered = []
    for product in products:
        # Search filter
        if search_term:
            if search_term.lower() not in product['name'].lower() and \
               search_term.lower() not in product['description'].lower():
                continue
        
        # Attribute filters
        if filters['vegan'] and not product['attributes']['vegan']:
            continue
        if filters['carbon_neutral'] and not product['attributes']['carbon_neutral']:
            continue
        if filters['fair_trade'] and not product['attributes']['fair_trade']:
            continue
        if filters['organic'] and not product['attributes']['organic']:
            continue
        if product['sustainability_rating'] < filters['min_rating']:
            continue
        
        filtered.append(product)
    
    return filtered

def add_to_cart(product):
    """Add product to cart"""
    for item in st.session_state.cart:
        if item['product_id'] == product['product_id']:
            item['quantity'] += 1
            persist_cart()
            return
    
    cart_item = product.copy()
    cart_item['quantity'] = 1
    st.session_state.cart.append(cart_item)
    persist_cart()

def remove_from_cart(product_id):
    """Remove product from cart"""
    st.session_state.cart = [item for item in st.session_state.cart 
                              if item['product_id'] != product_id]
    persist_cart()

def update_quantity(product_id, quantity):
    """Update quantity of item in cart"""
    if quantity == 0:
        remove_from_cart(product_id)
    else:
        for item in st.session_state.cart:
            if item['product_id'] == product_id:
                item['quantity'] = quantity
                break
        persist_cart()

def get_cart_total():
    """Calculate total cart price"""
    return sum(item['price'] * item['quantity'] for item in st.session_state.cart)

def get_cart_avg_rating():
    """Calculate average sustainability rating of cart items"""
    if not st.session_state.cart:
        return 0
    total_rating = sum(item['sustainability_rating'] for item in st.session_state.cart)
    return round(total_rating / len(st.session_state.cart))

def save_order():
    """Save order to database"""
    order = {
        "user_email": st.session_state.user['email'],
        "items": st.session_state.cart,
        "total": get_cart_total(),
        "avg_sustainability_rating": get_cart_avg_rating(),
        "created_at": datetime.datetime.now()
    }
    orders_collection.insert_one(order)
    # Clear persisted cart for the user
    try:
        if st.session_state.user:
            users_collection.update_one({"email": st.session_state.user['email']}, {"$set": {"cart": []}})
            st.session_state.user['cart'] = []
    except Exception:
        # don't crash the app if DB update fails
        pass


def persist_cart():
    """Persist the current session cart to the logged-in user's document."""
    try:
        if st.session_state.user:
            users_collection.update_one({"email": st.session_state.user['email']}, {"$set": {"cart": st.session_state.cart}})
            # Also update session user copy
            st.session_state.user['cart'] = st.session_state.cart
    except Exception:
        # silently ignore persistence errors during development
        pass