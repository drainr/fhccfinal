import streamlit as st
from pymongo import MongoClient
import os

@st.cache_resource
def init_connection():
    """Initialize MongoDB connection"""
    client = MongoClient(
    st.secrets["mongo_uri"],
    tls=True,
    tlsAllowInvalidCertificates=True
)
    return client

client = init_connection()
db = client.greenchoice_db

# Collections
users_collection = db.users
products_collection = db.products
orders_collection = db.orders

def init_sample_products():
    """Initialize the database with sample products"""
    if products_collection.count_documents({}) == 0:
        sample_products = [
            {
                "product_id": 1,
                "name": "Organic Cotton T-Shirt",
                "price": 29.99,
                "image": "https://img.sonofatailor.com/images/customizer/product/highneck/DarkGrey_Regular.jpg",
                "sustainability_rating": 92,
                "attributes": {
                    "vegan": True,
                    "carbon_neutral": True,
                    "fair_trade": True,
                    "organic": True,
                    "recycled_materials": False
                },
                "description": "Soft, breathable organic cotton t-shirt made with sustainable practices.",
                "category": "Clothing"
            },
            {
                "product_id": 2,
                "name": "Recycled Steel Water Bottle",
                "price": 24.99,
                "image": "https://m.media-amazon.com/images/I/31xGqwKcFfL.jpg",
                "sustainability_rating": 88,
                "attributes": {
                    "vegan": True,
                    "carbon_neutral": False,
                    "fair_trade": True,
                    "organic": False,
                    "recycled_materials": True
                },
                "description": "Eco-friendly bamboo exterior with stainless steel interior.",
                "category": "Home & Kitchen"
            },
            {
                "product_id": 3,
                "name": "Recycled Plastic Backpack",
                "price": 49.99,
                "image": "https://paktbags.com/cdn/shop/files/PDP_35L_Backpack-PAKT-6-14-23-25138_524dfb70-e013-4e6c-85aa-53080a4b1cab.jpg?v=1726097709",
                "sustainability_rating": 85,
                "attributes": {
                    "vegan": True,
                    "carbon_neutral": True,
                    "fair_trade": False,
                    "organic": False,
                    "recycled_materials": True
                },
                "description": "Durable backpack made from 100% recycled ocean plastic.",
                "category": "Accessories"
            },
            {
                "product_id": 4,
                "name": "Fair Trade Coffee Beans",
                "price": 16.99,
                "image": "https://centralperk.com/cdn/shop/products/med-dark_whole_right_1445x.png?v=1659993674",
                "sustainability_rating": 95,
                "attributes": {
                    "vegan": True,
                    "carbon_neutral": True,
                    "fair_trade": True,
                    "organic": True,
                    "recycled_materials": False
                },
                "description": "Ethically sourced, organic Arabica coffee beans.",
                "category": "Food & Beverage"
            },
            {
                "product_id": 5,
                "name": "Vegan Leather Wallet",
                "price": 34.99,
                "image": "https://www.graphicimage.com/cdn/shop/files/WLM-HAR-BRN-2_fd9e006c-47ad-4c6e-bb73-716e757542b4.jpg?v=1684737127",
                "sustainability_rating": 78,
                "attributes": {
                    "vegan": True,
                    "carbon_neutral": False,
                    "fair_trade": True,
                    "organic": False,
                    "recycled_materials": False
                },
                "description": "Stylish wallet made from sustainable plant-based materials.",
                "category": "Accessories"
            },
            {
                "product_id": 6,
                "name": "Solar-Powered Phone Charger",
                "price": 39.99,
                "image": "https://m.media-amazon.com/images/I/715gcpUyo-L._AC_UF894,1000_QL80_.jpg",
                "sustainability_rating": 90,
                "attributes": {
                    "vegan": True,
                    "carbon_neutral": True,
                    "fair_trade": False,
                    "organic": False,
                    "recycled_materials": True
                },
                "description": "Portable solar charger for on-the-go renewable energy.",
                "category": "Electronics"
            },
            {
                "product_id": 7,
                "name": "Organic Bamboo Toothbrush Set",
                "price": 12.99,
                "image": "https://m.media-amazon.com/images/I/51N9evzJYgL._AC_UF1000,1000_QL80_.jpg",
                "sustainability_rating": 93,
                "attributes": {
                    "vegan": True,
                    "carbon_neutral": True,
                    "fair_trade": False,
                    "organic": True,
                    "recycled_materials": False
                },
                "description": "Biodegradable bamboo toothbrushes, pack of 4.",
                "category": "Personal Care"
            },
            {
                "product_id": 8,
                "name": "Recycled Glass Food Containers",
                "price": 28.99,
                "image": "https://m.media-amazon.com/images/I/71RliRADeDL.jpg",
                "sustainability_rating": 87,
                "attributes": {
                    "vegan": True,
                    "carbon_neutral": False,
                    "fair_trade": False,
                    "organic": False,
                    "recycled_materials": True
                },
                "description": "Set of 3 food storage containers made from recycled glass.",
                "category": "Home & Kitchen"
            }
        ]
        
        low_quality_products = [
            {
                "product_id": 101,
                "name": "Polyester T-Shirt",
                "price": 14.99,
                "image": "https://northwestriders.com/cdn/shop/products/tee_6040_DkGryHth07.jpg?v=1547324771",
                "sustainability_rating": 38,
                "attributes": {
                    "vegan": True,
                    "carbon_neutral": False,
                    "fair_trade": False,
                    "organic": False,
                    "recycled_materials": False
                },
                "description": "Affordable polyester t-shirt. Cheaper, less sustainable alternative.",
                "category": "Clothing"
            },
            {
                "product_id": 102,
                "name": "Plastic Water Bottle",
                "price": 9.99,
                "image": "https://www.ecovessel.com/cdn/shop/files/EVWAVE24HB_Wave24oz_EastmanTritanPlasticWaterBottle_HudsonBlue.jpg?v=1724769575&width=2000",
                "sustainability_rating": 30,
                "attributes": {
                    "vegan": True,
                    "carbon_neutral": False,
                    "fair_trade": False,
                    "organic": False,
                    "recycled_materials": False
                },
                "description": "Low-cost plastic bottle.",
                "category": "Home & Kitchen"
            },
            {
                "product_id": 103,
                "name": "Polyester Backpack",
                "price": 24.99,
                "image": "https://www.nomatic.com/cdn/shop/files/TRPK14-NVY-01_TravelPack14L_NOMATIC_ECOMM_11.png?v=1754012389&width=320",
                "sustainability_rating": 35,
                "attributes": {
                    "vegan": True,
                    "carbon_neutral": False,
                    "fair_trade": False,
                    "organic": False,
                    "recycled_materials": False
                },
                "description": "Low-cost backpack made from mixed synthetic materials.",
                "category": "Accessories"
            },
            {
                "product_id": 104,
                "name": "Coffee Beans",
                "price": 8.99,
                "image": "https://cdn11.bigcommerce.com/s-4iv4za1ziu/images/stencil/original/products/119/8331/10oz-Breakfast-coffee-wholebean_web__68240.1692625348.jpg?c=1",
                "sustainability_rating": 28,
                "attributes": {
                    "vegan": True,
                    "carbon_neutral": False,
                    "fair_trade": False,
                    "organic": False,
                    "recycled_materials": False
                },
                "description": "Standard coffee beans with conventional sourcing.",
                "category": "Food & Beverage"
            },
            {
                "product_id": 105,
                "name": "Pleather Wallet",
                "price": 19.99,
                "image": "https://www.leatherology.com/cdn/shop/files/Thin-Bifold-Wallet-Black-115-135.jpg?v=1764174487",
                "sustainability_rating": 40,
                "attributes": {
                    "vegan": True,
                    "carbon_neutral": False,
                    "fair_trade": False,
                    "organic": False,
                    "recycled_materials": False
                },
                "description": "Inexpensive faux leather wallet with lower sustainability credentials.",
                "category": "Accessories"
            },
            {
                "product_id": 106,
                "name": "Portable Charger",
                "price": 19.99,
                "image": "https://i5.walmartimages.com/seo/Anker-PowerCore-Select-10000-Portable-Charger-Black-Ultra-Compact-High-Speed-Charging-Technology-Phone-Charger-for-iPhone-Samsung-and-More_621e9d8d-b4b2-4e15-b4cd-b439561ec4d0.c822834630c31c13416f2aacb33ddd5e.jpeg?odnHeight=768&odnWidth=768&odnBg=FFFFFF",
                "sustainability_rating": 45,
                "attributes": {
                    "vegan": True,
                    "carbon_neutral": False,
                    "fair_trade": False,
                    "organic": False,
                    "recycled_materials": False
                },
                "description": "Lower-cost solar/USB charger with standard manufacturing footprint.",
                "category": "Electronics"
            },
            {
                "product_id": 107,
                "name": "Plastic Toothbrush Pack",
                "price": 5.99,
                "image": "https://quantumlabs.com/images/thumbs/0010045_value-bulk-toothbrush-adult-and-junior-72-count.jpeg",
                "sustainability_rating": 25,
                "attributes": {
                    "vegan": True,
                    "carbon_neutral": False,
                    "fair_trade": False,
                    "organic": False,
                    "recycled_materials": False
                },
                "description": "Basic plastic toothbrushes, non-biodegradable.",
                "category": "Personal Care"
            },
            {
                "product_id": 108,
                "name": "Plastic Food Containers",
                "price": 12.99,
                "image": "https://i5.walmartimages.com/asr/0f4d1c4e-5b59-4652-8546-b10a7dddb6eb.2fd94d1f362b4090fa72ef53127c5392.jpeg",
                "sustainability_rating": 33,
                "attributes": {
                    "vegan": True,
                    "carbon_neutral": False,
                    "fair_trade": False,
                    "organic": False,
                    "recycled_materials": False
                },
                "description": "Lower-quality food containers with mixed materials.",
                "category": "Home & Kitchen"
            }
        ]

        products_collection.insert_many(sample_products + low_quality_products)


def init_session_state():
    """Initialize all session state variables"""
    if 'page' not in st.session_state:
        st.session_state.page = 'login'
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'cart' not in st.session_state:
        st.session_state.cart = []
    if 'selected_product' not in st.session_state:
        st.session_state.selected_product = None
    if 'filters' not in st.session_state:
        st.session_state.filters = {
            'vegan': False,
            'carbon_neutral': False,
            'fair_trade': False,
            'organic': False,
            'min_rating': 0
        }
    if 'search_term' not in st.session_state:
        st.session_state.search_term = ''