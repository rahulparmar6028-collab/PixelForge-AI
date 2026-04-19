import streamlit as st

st.markdown("""
    <style>
        .stApp { background-color: white; color: black; }
        .stButton > button { 
            background-color: #f0f2f6; 
            color: black !important; 
            border: 1px solid #cccccc;
        }
    </style>
""", unsafe_allow_html=True)

st.title("Image Generator")
st.text_input("Enter your prompt here...")
st.button("Generate Image")
st.image("https://via.placeholder.com/512", caption="Generated Image")