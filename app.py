import streamlit as st
import time, random, requests, io
from PIL import Image

# --- 1. AI HORDE CONFIGURATION ---
HORDE_API_KEY = "0000000000" 
HORDE_URL = "https://aihorde.net/api/v2/generate/async"

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="PixelForge AI", page_icon="🔮", layout="wide")

# --- INITIALIZE SESSION STATES ---
if "selected_style" not in st.session_state: st.session_state.selected_style = "None"
if "aspect_ratio" not in st.session_state: st.session_state.aspect_ratio = "None"
if "generated_images" not in st.session_state: st.session_state.generated_images = [None]
if "last_used_style" not in st.session_state: st.session_state.last_used_style = "None"
if "last_used_ratio" not in st.session_state: st.session_state.last_used_ratio = "None"
if "is_forging" not in st.session_state: st.session_state.is_forging = False
if "console_logs" not in st.session_state: st.session_state.console_logs = ["HORDE READY... STANDING BY"]
if "dark_mode" not in st.session_state: st.session_state.dark_mode = True
if "intensity" not in st.session_state: st.session_state.intensity = 7.5

def log_action(message):
    timestamp = time.strftime("%H:%M:%S")
    st.session_state.console_logs.append(f"[{timestamp}] > {message.upper()}")
    if len(st.session_state.console_logs) > 5: st.session_state.console_logs.pop(0)

# --- 2. THEME CONFIGURATION ---
p_color = "#a855f7" 
if st.session_state.dark_mode:
    bg_style = "linear-gradient(125deg, #0f172a 0%, #1e1b4b 25%, #4c1d95 50%, #831843 75%, #0f172a 100%)"
    text_c = "#ffffff"; card_bg = "rgba(255, 255, 255, 0.05)"; btn_header_bg = "#000000"
else:
    bg_style = "linear-gradient(135deg, #f3e8ff 0%, #fae8ff 33%, #fdf2f8 66%, #f5f3ff 100%)"
    text_c = "#2e1065"; card_bg = "rgba(255, 255, 255, 0.6)"; btn_header_bg = "#4c1d95"

st.markdown(f'''
<style>
.stApp {{ background: {bg_style}; background-attachment: fixed; color: {text_c}; transition: 0.8s ease; }}
.stButton > button, div[data-testid="stExpander"] details {{ background: {btn_header_bg} !important; border: 2px solid {p_color} !important; border-radius: 12px !important; color: #ffffff !important; font-weight: 950 !important; text-transform: uppercase !important; letter-spacing: 2px !important; }}
div.active-btn > div > button {{ background: #ffffff !important; color: {p_color} !important; box-shadow: 0 0 25px {p_color} !important; border: 3px solid #ffffff !important; transform: scale(1.05); }}
.hero-container {{ background: {card_bg}; backdrop-filter: blur(20px); border: 1px solid rgba(168, 85, 247, 0.3); border-radius: 35px; padding: 45px; text-align: center; margin-bottom: 25px; color: {text_c}; }}
.console-box {{ background: rgba(0,0,0,0.9); border: 1px solid {p_color}; border-radius: 15px; padding: 15px; font-family: monospace; color: {p_color}; font-size: 12px; margin-top: 30px; }}
.badge-container {{ display: flex; gap: 10px; margin-bottom: 10px; }}
.style-badge {{ background: {p_color}; color: white; padding: 5px 15px; border-radius: 20px; font-weight: 900; font-size: 11px; text-transform: uppercase; letter-spacing: 1px; }}
.ratio-badge {{ background: rgba(255,255,255,0.2); color: {text_c}; padding: 5px 15px; border-radius: 20px; border: 1px solid {p_color}; font-weight: 900; font-size: 11px; }}
label, .stMarkdown p {{ color: {text_c} !important; font-weight: 800 !important; }}
</style>
''', unsafe_allow_html=True)

# --- SIDEBAR & HEADER ---
with st.sidebar:
    st.markdown(f'<h1 style="color: {text_c}; font-weight: 900;">PixelForge</h1>', unsafe_allow_html=True)
    if st.toggle("MODE", value=st.session_state.dark_mode):
        if not st.session_state.dark_mode: st.session_state.dark_mode = True; st.rerun()
    else:
        if st.session_state.dark_mode: st.session_state.dark_mode = False; st.rerun()

st.markdown(f'<div class="hero-container"><h1>PIXELFORGE AI</h1></div>', unsafe_allow_html=True)

# --- INPUT SECTION ---
with st.container():
    _, input_col, _ = st.columns([1, 8, 1])
    with input_col:
        prompt = st.text_input("NEURAL VISION", placeholder="Enter vision...", key="main_prompt")
        neg_prompt = st.text_input("NEGATIVE DIRECTIVE", placeholder="Exclude...", key="neg_input")
        if st.button("EXECUTE FORGE", use_container_width=True):
            if prompt: 
                # Immediate Badge Lock-in
                st.session_state.last_used_style = st.session_state.selected_style
                st.session_state.last_used_ratio = st.session_state.aspect_ratio
                st.session_state.is_forging = True
                log_action("Broadcasting Request...")
                st.rerun()

# --- SELECTORS ---
neural_themes = {
    "None": "", "Cinematic": "cinematic lighting", "Anime": "anime style", "3D Render": "unreal engine 5",
    "Cyberpunk": "cyberpunk neon", "Fantasy": "epic fantasy", "Oil Paint": "oil on canvas",
    "Vaporwave": "vaporwave pastel", "Sketch": "pencil sketch", "Steampunk": "steampunk gears"
}

with st.container():
    _, col_main, _ = st.columns([1, 8, 1])
    with col_main:
        st.markdown(f'<p style="font-size:11px; font-weight:900;">CANVAS RATIO</p>', unsafe_allow_html=True)
        r_list = ["None", "1:1", "16:9", "9:16"]
        r_cols = st.columns(4)
        for i, r in enumerate(r_list):
            with r_cols[i]:
                is_active = "active-btn" if st.session_state.aspect_ratio == r else ""
                st.markdown(f'<div class="{is_active}">', unsafe_allow_html=True)
                if st.button(r, key=f"rat_{r}", use_container_width=True):
                    st.session_state.aspect_ratio = r; st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

        st.markdown(f'<p style="font-size:11px; font-weight:900; margin-top:15px;">NEURAL THEMES</p>', unsafe_allow_html=True)
        theme_names = list(neural_themes.keys())
        r_cols = [st.columns(5), st.columns(5)]
        for i, name in enumerate(theme_names):
            col = r_cols[0][i] if i < 5 else r_cols[1][i-5]
            with col:
                is_active = "active-btn" if st.session_state.selected_style == name else ""
                st.markdown(f'<div class="{is_active}">', unsafe_allow_html=True)
                if st.button(name, key=f"theme_{name}", use_container_width=True):
                    st.session_state.selected_style = name; st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

# --- FORGING LOGIC ---
if st.session_state.is_forging:
    with st.spinner("Forging Neural Pathways..."):
        try:
            dim_map = {"None": (512, 512), "1:1": (512, 512), "16:9": (640, 384), "9:16": (384, 640)}
            w, h = dim_map.get(st.session_state.last_used_ratio, (512, 512))
            headers = {"apikey": HORDE_API_KEY, "Client-Agent": "PixelForge:1.0:AI"}
            style_prompt = neural_themes[st.session_state.last_used_style]
            payload = {
                "prompt": f"{prompt}, {style_prompt} ### {neg_prompt}",
                "params": {"cfg_scale": st.session_state.intensity, "width": w, "height": h, "steps": 25}
            }
            submit = requests.post(HORDE_URL, json=payload, headers=headers)
            job_id = submit.json()['id']
            done = False
            while not done:
                check = requests.get(f"https://aihorde.net/api/v2/generate/check/{job_id}").json()
                if check['done']:
                    status = requests.get(f"https://aihorde.net/api/v2/generate/status/{job_id}").json()
                    img_data = requests.get(status['generations'][0]['img']).content
                    st.session_state.generated_images[0] = Image.open(io.BytesIO(img_data))
                    log_action("Neural Link: SUCCESS")
                    done = True
                else:
                    time.sleep(4)
        except Exception as e: log_action("Link Error")
        st.session_state.is_forging = False; st.rerun()

# --- MASTER CANVAS (BADGES ALWAYS VISIBLE DURING FORGE) ---
st.write("---")
_, center_col, _ = st.columns([1, 6, 1])
with center_col:
    with st.expander("Neural Output • Master Canvas", expanded=True):
        # Show badges if currently forging OR if an image exists
        if st.session_state.is_forging or st.session_state.generated_images[0]:
            st.markdown(f'''
            <div class="badge-container">
                <div class="style-badge">STYLE: {st.session_state.last_used_style}</div>
                <div class="ratio-badge">RATIO: {st.session_state.last_used_ratio}</div>
            </div>
            ''', unsafe_allow_html=True)
            
        if st.session_state.generated_images[0]:
            st.image(st.session_state.generated_images[0], use_container_width=True)
        else:
            st.markdown('<div style="height: 300px; border: 2px dashed #a855f7; display: flex; align-items: center; justify-content: center; font-weight: 900;">AWAITING NEURAL SIGNAL</div>', unsafe_allow_html=True)
        
        st.write("---")
        st.session_state.intensity = st.slider("NEURAL INTENSITY", 1.0, 20.0, 7.5, 0.5)
        v_col, e_col = st.columns(2)
        with v_col:
            if st.button("VARIANT", use_container_width=True):
                if prompt: 
                    st.session_state.last_used_style = st.session_state.selected_style
                    st.session_state.last_used_ratio = st.session_state.aspect_ratio
                    st.session_state.is_forging = True
                    st.rerun()
        with e_col:
            if st.session_state.generated_images[0]:
                buf = io.BytesIO(); st.session_state.generated_images[0].save(buf, format="PNG")
                st.download_button("EXPORT PNG", buf.getvalue(), "pixel_forge.png", "image/png", use_container_width=True)

st.markdown('<div class="console-box">', unsafe_allow_html=True)
for log in st.session_state.console_logs: st.markdown(f'<div style="font-weight:900;">{log}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)