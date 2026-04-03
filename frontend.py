import streamlit as st
import requests

# 1. INITIALIZATION & LAYOUT
st.set_page_config(page_title="Nexus AI", layout="wide")

# Define the Live Render URL
URL = "https://nexus-ai-1-3rxu.onrender.com/chat"

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi there, how can I assist you today?"}
    ]

# 2. CUSTOM STYLING 
st.markdown("""
    <style>
    .stChatMessage {
        color: white !important;
        background-color: #262730 !important;
    }
    div[data-testid="stPopover"] > button {
        border-radius: 50% !important;
        background-color: transparent !important;
        border: none !important;
        font-size: 24px !important;
    }
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# 3. TOP HISTORY SECTION
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
        prompt = st.text_input("Ask Nexus", key="user_prompt", label_visibility="collapsed", placeholder="Ask Nexus...")

    with c3:
        st.selectbox("Mode", ["Fast ▾", "Quality"], label_visibility="collapsed", key="mode")

    with c4:
        send_btn = st.button("➤")

# 5. LOGIC: HANDLING THE MESSAGE
if (send_btn or prompt) and prompt:
    # Prevent duplicate messages
    if "last_sent" not in st.session_state or st.session_state.last_sent != prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.last_sent = prompt 
        
        try:
            # Added a spinner to tell the user the AI is "waking up"
            with st.spinner("Nexus is waking up... this may take a minute..."):
                # Added timeout=60 to wait for Render's free tier to start
                response = requests.post(URL, params={"user_input": prompt}, timeout=60)
                
            if response.status_code == 200:
                ans = response.json().get("response")
                st.session_state.messages.append({"role": "assistant", "content": ans})
            else:
                st.error(f"Nexus is busy (Error {response.status_code}). Please try again.")
        except Exception as e:
            st.error("Backend connection failed. Render might still be waking up.")
            print(f"Error: {e}")

        st.rerun()
