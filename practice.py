import streamlit as st
import time, requests, io, os, hashlib, json, random  # Added 'random' here
from PIL import Image
from dotenv import load_dotenv

# --- 1. SYSTEM CONFIGURATION ---
load_dotenv()
HORDE_API_KEY = os.getenv("HORDE_API_KEY")
HF_TOKEN = os.getenv("HF_TOKEN")
USER_DB = "users.json"

if not os.path.exists(USER_DB):
    with open(USER_DB, "w") as f: json.dump({}, f)

st.set_page_config(page_title="PixelForge AI", layout="wide", page_icon="🔮")

# --- INITIALIZE SESSION STATES ---
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "username" not in st.session_state: st.session_state.username = ""
if "generated_image" not in st.session_state: st.session_state.generated_image = None
if "logs" not in st.session_state: st.session_state.logs = []

def log(msg):
    st.session_state.logs.append(f"[{time.strftime('%H:%M:%S')}] {msg}")

# --- AUTHENTICATION ---
if not st.session_state.logged_in:
    st.title("🔮 PIXELFORGE ACCESS")
    user = st.text_input("USERNAME")
    pw = st.text_input("PASSWORD", type="password")
    if st.button("ENTER TERMINAL", use_container_width=True):
        h_pw = hashlib.sha256(str.encode(pw)).hexdigest()
        with open(USER_DB, "r") as f: db = json.load(f)
        if user in db and db[user] == h_pw:
            st.session_state.logged_in = True; st.session_state.username = user; st.rerun()
        else:
            db[user] = h_pw
            with open(USER_DB, "w") as f: json.dump(db, f)
            st.session_state.logged_in = True; st.session_state.username = user; st.rerun()

else:
    # --- MAIN UI ---
    with st.sidebar:
        st.header("⚡ PIXELFORGE")
        st.write(f"OPERATOR: **{st.session_state.username.upper()}**")
        engine = st.selectbox("ENGINE", ["Pollinations (Guaranteed)", "AI Horde", "Hugging Face (Experimental)"])
        if st.button("LOGOUT"): st.session_state.logged_in = False; st.rerun()

    st.title("PIXELFORGE AI")
    prompt = st.text_input("NEURAL VISION", placeholder="Enter your prompt...")

    if st.button("EXECUTE FORGE", use_container_width=True):
        if not prompt:
            st.warning("Please enter a prompt.")
        else:
            with st.spinner("FORGING..."):
                try:
                    # --- ENGINE 1: POLLINATIONS (Fast & Free) ---
                    if engine == "Pollinations (Guaranteed)":
                        # Direct GET request - the most stable way to generate images
                        seed = random.randint(1, 999999)
                        url = f"https://image.pollinations.ai/prompt/{prompt.replace(' ', '%20')}?width=1024&height=1024&seed={seed}&nologo=true"
                        response = requests.get(url, timeout=30)
                        if response.status_code == 200:
                            st.session_state.generated_image = Image.open(io.BytesIO(response.content))
                            log("Pollinations: Forge Success")
                        else:
                            st.error(f"Pollinations Error: {response.status_code}")

                    # --- ENGINE 2: AI HORDE ---
                    elif engine == "AI Horde":
                        res = requests.post("https://aihorde.net/api/v2/generate/async", 
                                           json={"prompt": prompt}, headers={"apikey": HORDE_API_KEY})
                        jid = res.json().get('id')
                        if jid:
                            for i in range(15):
                                chk = requests.get(f"https://aihorde.net/api/v2/generate/check/{jid}").json()
                                if chk.get('done'):
                                    stat = requests.get(f"https://aihorde.net/api/v2/generate/status/{jid}").json()
                                    img_url = stat['generations'][0]['img']
                                    st.session_state.generated_image = Image.open(io.BytesIO(requests.get(img_url).content))
                                    log("Horde: Forge Success")
                                    break
                                time.sleep(3)

                    # --- ENGINE 3: HUGGING FACE (Using Router URL) ---
                    elif engine == "Hugging Face (Experimental)":
                        # UPDATED ROUTER URL
                        API_URL = "https://router.huggingface.co/hf-inference/v1/models/stabilityai/stable-diffusion-xl-base-1.0"
                        headers = {"Authorization": f"Bearer {HF_TOKEN}", "Content-Type": "application/json"}
                        response = requests.post(API_URL, headers=headers, json={"inputs": prompt}, timeout=60)
                        if response.status_code == 200:
                            st.session_state.generated_image = Image.open(io.BytesIO(response.content))
                            log("HF: Forge Success")
                        else:
                            st.error(f"HF Router Error {response.status_code}: {response.text}")

                except Exception as e:
                    st.error(f"Forge Failed: {str(e)}")
                    log(f"Critical Error: {str(e)}")

    # --- CANVAS ---
    if st.session_state.generated_image:
        st.image(st.session_state.generated_image, use_container_width=True)
        buf = io.BytesIO()
        st.session_state.generated_image.save(buf, format="PNG")
        st.download_button("DOWNLOAD PNG", buf.getvalue(), "pixel_forge.png", "image/png")

    # --- LOGS ---
    with st.expander("System Logs"):
        for l in st.session_state.logs:
            st.text(l)