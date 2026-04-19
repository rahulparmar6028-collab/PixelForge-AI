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