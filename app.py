<<<<<<< HEAD
import streamlit as st
import os, random, requests, io, json, time
from PIL import Image
from dotenv import load_dotenv

# Import our custom modules
import logic
import styles
import components

# --- CINEMATIC LUXURY PALETTE ---
CRIMSON = "#a6445d"
DEEP_SEA = "#142f40"
STEEL_BLUE = "#62929E"
SAGE = "#393A10"
SANDSTONE = "#E7DECD"

# --- 1. CONFIG & SYSTEM ---
load_dotenv()
HORDE_API_KEY = os.getenv("HORDE_API_KEY")

st.set_page_config(page_title="PixelForge AI", page_icon="None", layout="wide")
styles.apply_pro_theme()

# --- 2. SESSION STATE ---
saved_user = logic.check_active_session()
if "logged_in" not in st.session_state: st.session_state.logged_in = True if saved_user else False
if "username" not in st.session_state: st.session_state.username = saved_user if saved_user else ""
if "prompt_val" not in st.session_state: st.session_state.prompt_val = ""
if "neg_val" not in st.session_state: st.session_state.neg_val = "blurry, low quality"
if "generated_images" not in st.session_state: st.session_state.generated_images = [None]
if "is_forging" not in st.session_state: st.session_state.is_forging = False
if "console_logs" not in st.session_state: st.session_state.console_logs = ["SYSTEM READY"]
if "seed_val" not in st.session_state: st.session_state.seed_val = -1
if "history" not in st.session_state: st.session_state.history = []
if "var_seed_val" not in st.session_state: st.session_state.var_seed_val = -1
if "var_strength" not in st.session_state: st.session_state.var_strength = 0.1

# --- 3. GATEWAY ---
if not st.session_state.logged_in:
    st.markdown('<div class="hero-container"><h1>PIXELFORGE AI</h1></div>', unsafe_allow_html=True)
    mode = st.radio("GATEWAY", ["LOGIN", "SIGNUP", "FORGOT PASSWORD"], horizontal=True)
    with st.container():
        _, col, _ = st.columns([1, 2, 1])
        with col:
            if mode == "SIGNUP":
                n_u = st.text_input("USERNAME")
                n_p = st.text_input("PASSWORD", type="password")
                sec = st.text_input("SECRET KEY")
                if st.button("CREATE ACCOUNT", use_container_width=True):
                    with open(logic.USER_DB, "r") as f: db = json.load(f)
                    db[n_u] = {"pw": logic.make_hashes(n_p), "secret": logic.make_hashes(sec.lower().strip())}
                    json.dump(db, open(logic.USER_DB, "w")); st.success("Created!")
            elif mode == "LOGIN":
                u = st.text_input("USERNAME")
                p = st.text_input("PASSWORD", type="password")
                if st.button("ENTER TERMINAL", use_container_width=True):
                    with open(logic.USER_DB, "r") as f: db = json.load(f)
                    if u in db and logic.check_hashes(p, db[u]["pw"]):
                        st.session_state.logged_in = True; st.session_state.username = u
                        logic.save_active_session(u); st.rerun()
                    else: st.error("Denied")
            # ... Forgot Password logic would go here similarly ...

else:
    # --- UI COMPONENTS ---
    components.render_sidebar()
    
    tab1, tab2 = st.tabs(["FORGE TERMINAL", "DOCUMENTATION"])

    with tab1:
        st.markdown('<div class="hero-container"><h1>PIXELFORGE AI</h1></div>', unsafe_allow_html=True)
        
        u_p = st.text_input("NEURAL VISION", value=st.session_state.prompt_val)
        if st.button("ENHANCE PROMPT"):
            p_pool = ["8k resolution", "raytraced", "cinematic lighting", "ultra-detailed", "photorealistic", "masterpiece"]
            st.session_state.prompt_val = logic.smart_enhance(u_p, p_pool)
            st.rerun()
        
        u_n = st.text_input("NEGATIVE DIRECTIVE", value=st.session_state.neg_val)
        if st.button("ENHANCE NEGATIVE"):
            n_pool = ["blurry", "low quality", "bad anatomy", "distorted", "extra limbs", "watermark", "grainy"]
            st.session_state.neg_val = logic.smart_enhance(u_n, n_pool)
            st.rerun()

        neural_themes = {"Realistic": "photorealistic", "Cinematic": "dramatic", "Anime": "anime", "Cyberpunk": "neon synthwave"}
        model_map = {
            "Standard": "stable_diffusion",
            "Photo-Pro (ICBINP)": "ICBINP - I Can't Believe It's Not Photography",
            "Reality-Focus": "Realistic Vision V6.0"
        }

        with st.expander("ENGINE CONFIGURATION", expanded=True):
            col1, col2, col3 = st.columns(3)
            with col1: ratio = st.select_slider("ASPECT RATIO", options=["1:1", "16:9", "9:16"])
            with col2: theme = st.selectbox("STYLE PRESET", options=list(neural_themes.keys()))
            with col3: selected_model = st.selectbox("NEURAL ENGINE", options=list(model_map.keys()))

        if st.button("EXECUTE FORGE", use_container_width=True):
            st.session_state.generated_images[0] = None
            if u_p: st.session_state.is_forging = True; st.rerun()

        # --- THE FORGING ENGINE ---
        if st.session_state.is_forging:
            # Applying the Cinematic gradient to the progress bar
            st.markdown(f'''<style>stProgress > div > div > div > div {{ background-image: linear-gradient(to right, {STEEL_BLUE}, {CRIMSON}); }}</style>''', unsafe_allow_html=True)
            
            p_bar = st.progress(0); s_text = st.empty()
            try:
                dim_map = {"1:1": (512, 512), "16:9": (640, 384), "9:16": (384, 640)}
                w, h = dim_map.get(ratio, (512, 512))
                cur_seed = str(random.randint(1, 10**9)) if st.session_state.seed_val == -1 else str(st.session_state.seed_val)
                
                full_prompt = f"{u_p}, {neural_themes[theme]}, masterpiece, 8k ### {u_n}"
                payload = {
                    "prompt": full_prompt,
                    "params": {
                        "width": int(w), "height": int(h), "steps": 30, "seed": cur_seed,
                        "variation_seed": int(random.randint(1, 10**9) if st.session_state.var_seed_val == -1 else st.session_state.var_seed_val),
                        "variation_amount": float(st.session_state.var_strength),
                        "sampler_name": "k_dpmpp_2m", "cfg_scale": 7.5
                    },
                    "models": [model_map[selected_model]]
                }
                
                res = requests.post("https://aihorde.net/api/v2/generate/async", json=payload, headers={"apikey": HORDE_API_KEY if HORDE_API_KEY else "0000000000"})
                if res.status_code == 202:
                    jid = res.json()['id']
                    for i in range(1, 101):
                        time.sleep(1)
                        chk = requests.get(f"https://aihorde.net/api/v2/generate/check/{jid}").json()
                        if chk['done']:
                            status = requests.get(f"https://aihorde.net/api/v2/generate/status/{jid}").json()
                            img_url = status['generations'][0]['img']
                            img = Image.open(io.BytesIO(requests.get(img_url).content))
                            st.session_state.generated_images[0] = img
                            st.session_state.history.append({"img": img, "prompt": u_p, "seed": cur_seed})
                            logic.log_action(f"Forge Success: {selected_model}"); break
                        else:
                            p_bar.progress(min(i * 2, 95))
                            s_text.text(f"Queue: {chk.get('queue_position')} | Wait: {chk.get('wait_time')}s")
                else:
                    logic.log_action(f"API Error: {res.status_code}")
            except Exception as e: st.error(f"Error: {e}")
            st.session_state.is_forging = False; st.rerun()

        if st.session_state.generated_images[0]:
            st.image(st.session_state.generated_images[0], use_container_width=True)

    with tab2:
        components.render_knowledge_hub()

    components.render_console()
=======
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
>>>>>>> cf97a5ab36271ed12e4611cbe0d7411c2ea5ecbd
