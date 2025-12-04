import streamlit as st

def load_css():
    st.markdown("""
        <style>
        .product-card {
            border: 1px solid #e0e0e0;
            border-radius: 10px;
            padding: 15px;
            margin: 10px 0;
            background: white;
        }
        .rating-badge {
            display: inline-block;
            padding: 5px 12px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 14px;
        }
        .rating-high { background: #d4edda; color: #155724; }
        .rating-medium { background: #fff3cd; color: #856404; }
        .rating-low { background: #f8d7da; color: #721c24; }
        .attribute-badge {
            display: inline-block;
            padding: 3px 10px;
            margin: 3px;
            border-radius: 15px;
            font-size: 12px;
        }
        .badge-vegan { background: #d4edda; color: #155724; }
        .badge-carbon { background: #cfe2ff; color: #084298; }
        .badge-fair { background: #e2d9f3; color: #432874; }
        .badge-organic { background: #d1e7dd; color: #0f5132; }
        .badge-recycled { background: #cff4fc; color: #055160; }
        .stButton>button {
            width: 100%;
        }
        </style>
    """, unsafe_allow_html=True)