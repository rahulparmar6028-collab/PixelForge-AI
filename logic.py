import streamlit as st
import hashlib, json, time, random, requests, io
from PIL import Image

USER_DB = "users.json"
SESSION_DB = "active_sessions.json"

# --- AUTH & SESSION LOGIC ---
def make_hashes(password): 
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password, hashed_text): 
    return make_hashes(password) == hashed_text

def save_active_session(username):
    with open(SESSION_DB, "r") as f: db = json.load(f)
    db["current_user"] = username
    with open(SESSION_DB, "w") as f: json.dump(db, f)

def check_active_session():
    try:
        with open(SESSION_DB, "r") as f: return json.load(f).get("current_user")
    except: return None

# --- PROMPT LOGIC ---
def smart_enhance(current_text, pool):
    tags = [t.strip().lower() for t in current_text.split(",") if t.strip()]
    available = [p for p in pool if p.lower() not in tags]
    if available:
        new_picks = random.sample(available, min(len(available), 2))
        tags.extend(new_picks)
    seen = set()
    unique_tags = [t for t in tags if not (t in seen or seen.add(t))]
    return ", ".join(unique_tags)

# --- SYSTEM LOGIC ---
def log_action(message):
    if "console_logs" not in st.session_state:
        st.session_state.console_logs = []
    # Removed the ">" to make it look like a professional system log
    st.session_state.console_logs.append(f"[{time.strftime('%H:%M:%S')}] {message.upper()}")
    if len(st.session_state.console_logs) > 5: 
        st.session_state.console_logs.pop(0)