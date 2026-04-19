import streamlit as st

def apply_pro_theme():
    # Cinematic Luxury Palette
    crimson = "#a6445d"
    deep_sea = "#142f40"
    steel_blue = "#62929E"
    sage = "#393A10"
    sandstone = "#E7DECD"
    sky_blue = "#bdcddc"
    
    st.markdown(f'''<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&family=Playfair+Display:wght@900&family=JetBrains+Mono&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Public+Sans:wght@400;700&family=Syncopate:wght@700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,wght@0,900;1,900&family=Montserrat:wght@300;500&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&family=Space+Grotesk:wght@700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@700&family=DM+Sans:wght@400;700&display=swap');

    /* 1. Deep Sea Foundation */
    .stApp {{ 
        background-color: {deep_sea};
        background-image: linear-gradient(180deg, {deep_sea} 0%, #0a1a24 100%);
        color: {sandstone}; 
        font-family: 'Inter', sans-serif !important;
    }}

    /* GLOBAL HEADERS - Playfair Display */
    h1, h2, h3 {{
        font-family: 'Playfair Display', serif !important;
        font-weight: 900 !important;
        letter-spacing: -0.5px !important;
    }}

    /* 2. Glassmorphism Sidebar with Steel Blue Glow */
    section[data-testid="stSidebar"] {{
        background-color: rgba(20, 47, 64, 0.8) !important;
        backdrop-filter: blur(15px);
        border-right: 1px solid {steel_blue}33;
    }}

    /* 3. Sandstone Terminal (The Canvas) */
    .hero-container {{ 
        background: rgba(231, 222, 205, 0.2) !important;
        backdrop-filter: blur(15px);
        border: 5px solid rgba(166, 68, 93, 0.3);
        border-radius: 4px; 
        padding: 40px; 
        margin-bottom: 25px; 
        border-left: 8px solid {crimson};
        box-shadow: 20px 20px 0px rgba(0,0,0,0.1);
        text-align: center;
    }}
    .hero-container h1 {{
        color: {sky_blue} !important;
        font-family: 'Syncopate', serif !important;
        font-weight: 900 !important;
        letter-spacing: 4px !important;
        text-transform: uppercase;
        text-align: center;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
        margin: 0 auto;
    }}

    /* 4. Crimson Execute Button (The Signature Action) */
    .stButton > button {{ 
        background: {crimson} !important; 
        color: white !important; 
        border: 2px solid {sky_blue} !important;
        border-radius: 2px !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 2px !important;
        transition: all 0.3s ease;
        width: 100%;
    }}
    .stButton > button:hover {{
        background: {deep_sea} !important;
        color: {sandstone} !important;
        transform: scale(1.01);
    }}

    /* 5. Steel Blue Accents for Secondary Buttons */
    div.stButton > button[key^="enhance"] {{
        background: transparent !important;
        color: {steel_blue} !important;
        border: 1px solid {steel_blue} !important;
    }}

    /* 6. Sage Console (Organic Logic) */
    .console-box {{ 
        background: {sage}; 
        border: 1px solid rgba(231, 222, 205, 0.2);
        color: {sandstone};
        border-radius: 0px;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 11px !important;
        opacity: 0.9;
    }}
    
    /* Inputs matching the Sandstone Workspace */
    .stTextInput > div > div > input {{
        background-color: white !important;
        border: 1px solid #ccc !important;
        color: {deep_sea} !important;
        border-radius: 0px !important;
        font-family: 'Inter', sans-serif !important;
        caret-color: {crimson} !important; /* FIXED: Blinking cursor is now visible */
    }}
    
    /* Input Label refinement */
    label p {{
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}
    </style>''', unsafe_allow_html=True)