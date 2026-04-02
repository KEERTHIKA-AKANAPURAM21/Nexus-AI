import streamlit as st
import requests

# 1. INITIALIZATION & LAYOUT
# Updated page title to Nexus
st.set_page_config(page_title="Nexus AI", layout="wide")

# This keeps track of every chat "matter"
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi there, how can I assist you today?"}
    ]

# 2. CUSTOM STYLING 
st.markdown("""
    <style>
    /* Make the chat history area scrollable */
    .stMain {
        background-color: #131314;
        color: #e3e3e3;
    }
    /* Style the Plus Button */
    div[data-testid="stPopover"] > button {
        border-radius: 50% !important;
        background-color: transparent !important;
        border: none !important;
        font-size: 24px !important;
    }
    /* Fixed Bottom Bar Styling */
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# 3. TOP HISTORY SECTION
# Updated Title to Nexus
st.title("Nexus AI")

chat_history_area = st.container()

with chat_history_area:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

# 4. THE FUNCTIONAL BOTTOM BAR
st.markdown("<br><br><br><br>", unsafe_allow_html=True)

with st.container():
    c1, c2, c3, c4 = st.columns([0.6, 10, 1.5, 0.8], vertical_alignment="center")

    with c1:
        with st.popover("＋"):
            st.markdown("##### Upload files")
            up_file = st.file_uploader("Upload", label_visibility="collapsed", key="active_up", type=["pdf", "png", "jpg"])
            if up_file:
                st.success(f"Attached: {up_file.name}")

            st.link_button("🔺 Add from Drive", "https://drive.google.com", use_container_width=True)

            if st.button("📷 Take photo", use_container_width=True, key="btn_photo"):
                st.session_state.active_action = "camera"
                
            if st.session_state.get("active_action") == "camera":
                cam_img = st.camera_input("Smile!", label_visibility="collapsed")
                if cam_img:
                    st.success("Photo captured!")
                    st.session_state.active_action = None 

            st.link_button("🌀 NotebookLM", "https://notebooklm.google.com", use_container_width=True)
            
    with c2:
        # Updated placeholder to "Ask Nexus"
        prompt = st.text_input("Ask Nexus", key="user_prompt", label_visibility="collapsed", placeholder="Ask Nexus...")

    with c3:
        st.selectbox("Mode", ["Fast ▾", "Quality"], label_visibility="collapsed", key="mode")

    with c4:
        send_btn = st.button("➤")

# 5. LOGIC: STOPPING THE LOOP & ADDING TO HISTORY
if (send_btn or prompt) and prompt:
    if "last_sent" not in st.session_state or st.session_state.last_sent != prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.last_sent = prompt 
        
        try:
            # During local testing use this:
            response = requests.post("http://127.0.0.1:8000/chat", params={"user_input": prompt})
            if response.status_code == 200:
                ans = response.json().get("response")
                st.session_state.messages.append({"role": "assistant", "content": ans})
            else:
                st.error("Nexus is currently busy. Please try again in a moment.")
        except:
            st.error("Backend connection failed. Ensure Nexus Backend is running.")

        st.rerun()