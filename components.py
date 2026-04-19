import streamlit as st

def render_sidebar():
    with st.sidebar:
        st.write(f"**OPERATOR:** {st.session_state.username.upper()}")
        if st.button("LOGOUT", use_container_width=True):
            import json
            with open("active_sessions.json", "w") as f: json.dump({}, f)
            st.session_state.logged_in = False
            st.rerun()
        
        st.write("---")
        st.subheader("History")
        for idx, item in enumerate(reversed(st.session_state.history)):
            st.markdown('<div class="history-card">', unsafe_allow_html=True)
            st.image(item["img"], caption=f"Seed: {item['seed']}", use_container_width=True)
            if st.button(f"REUSE #{len(st.session_state.history)-idx}", key=f"h_{idx}", use_container_width=True):
                st.session_state.prompt_val = item["prompt"]
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
            
        st.write("---")
        st.subheader("DNA CONTROL")
        use_rand = st.checkbox("Randomize Primary Seed", value=(st.session_state.seed_val == -1))
        
        if not use_rand:
            s_input = st.number_input("Primary Seed", value=12345 if st.session_state.seed_val == -1 else st.session_state.seed_val)
            st.session_state.seed_val = int(s_input)
        else:
            st.session_state.seed_val = -1

        st.write("---")
        st.caption("SECONDARY DNA (VARIATION)")
        v_seed_input = st.number_input("Variation Seed", value=-1)
        st.session_state.var_seed_val = int(v_seed_input)
        
        v_strength = st.slider("Variation Strength", 0.0, 1.0, 0.1)
        st.session_state.var_strength = v_strength

def render_console():
    st.write("---")
    st.markdown(f'<div class="console-box" style="background-color: #393A10; color: #E7DECD; border: 1px solid #62929E;">', unsafe_allow_html=True)
    for l in st.session_state.console_logs:
        st.markdown(f'<div style="font-family: monospace; font-size: 11px; padding: 2px;">{l}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def render_knowledge_hub():
    st.header("Knowledge Hub")
    st.write("---")
    with st.expander("DNA Control (Seed Selection)", expanded=True):
        st.write("The Seed is a critical integer that serves as the base for the initial noise. Every AI image starts as a field of random static; the seed number acts as a 'coordinate' that determines the exact pattern. For professional workflows, Seed Locking is essential for iterative design. When you fix a seed, you are freezing the spatial composition, allowing you to modify the text prompt while keeping the primary subject identical.")
    
    with st.expander("Prompt Enhancement", expanded=True):
        st.write("Prompt Enhancement is the bridge between a simple idea and a high-fidelity output. Directing an AI requires 'technical steering.' When you use the Enhance feature, the system injects weighted tokens like 'Raytracing' or '8k Resolution' that prioritize high-quality training data, resulting in sharper textures and professional-grade composition.")
    
    with st.expander("Negative Directives", expanded=True):
        st.write("The Negative Directive field is a 'Quality Guard.' While the positive prompt tells the AI what to create, the negative prompt tells it which mathematical paths to avoid. By prepending negatives like 'lowres, distorted, extra limbs,' you are instructing the algorithm to reject amateur artifacts, significantly reducing the need for repeated re-rolls.")

    with st.expander("Neural Archive", expanded=True):
        st.write("The Neural Archive is your session’s temporal database for comparative analysis. The Archive stores the last five artifacts, including their specific Seed and Prompt metadata. Clicking 'Reuse' re-populates the input fields with the exact 'chemical formula' used for that specific generation, turning the artistic process into a scientific one.")