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

# 2. CUSTOM STYLING - Fixed Visibility
# 2. CUSTOM STYLING - Hidden Toolbar & Fixed Visibility
# 2. CUSTOM STYLING - Clean Interface
# 2. CUSTOM STYLING - Targeted Hide
# 2. CUSTOM STYLING - Targeted Cleanup
# 2. CUSTOM STYLING - Targeted Cleanup & Profile Look
st.markdown("""
    <style>
    /* 1. HIDE GITHUB, PENCIL, AND MANAGE APP */
    div[data-testid="stToolbar"], 
    div[data-testid="stStatusWidget"] {
        display: none !important;
    }

    /* 2. ENSURE SHARE & THREE DOTS REMAIN VISIBLE */
    header[data-testid="stHeader"] {
        visibility: visible !important;
    }

    /* 3. CHAT BUBBLE VISIBILITY */
    .stChatMessage {
        background-color: #f0f2f6 !important;
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 10px;
    }
    .stChatMessage p {
        color: #1E1E1E !important; 
    }

    /* 4. HIDE FOOTER */
    footer {visibility: hidden;}

    /* 5. STYLE THE PLUS BUTTON */
    div[data-testid="stPopover"] > button {
        border-radius: 50% !important;
        background-color: transparent !important;
        border: none !important;
        font-size: 24px !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. TOP SECTION WITH NEW CHAT FUNCTION
col_title, col_new_chat = st.columns([9, 1])



with col_new_chat:
    # Adding a "New Chat" button that clears the session
    if st.button("➕", help="Start a New Chat"):
        st.session_state.messages = [{"role": "assistant", "content": "Hi there, how can I assist you today?"}]
        st.rerun()

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
            
    with c2:
        prompt = st.text_input("Ask Nexus", key="user_prompt", label_visibility="collapsed", placeholder="Ask Nexus...")

    with c3:
        st.selectbox("Mode", ["Fast ▾", "Quality"], label_visibility="collapsed", key="mode")

    with c4:
        send_btn = st.button("➤")

# 5. LOGIC: HANDLING THE MESSAGE
if (send_btn or prompt) and prompt:
    # Add user message to state immediately
    if "last_sent" not in st.session_state or st.session_state.last_sent != prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.last_sent = prompt 
        
        try:
            with st.spinner("Nexus is thinking..."):
                # Timeout set to 20 seconds as requested
                response = requests.post(URL, params={"user_input": prompt}, timeout=20)
                
            if response.status_code == 200:
                ans = response.json().get("response")
                st.session_state.messages.append({"role": "assistant", "content": ans})
            else:
                st.error(f"Backend Error ({response.status_code}). Try again.")
        except requests.exceptions.Timeout:
            st.warning("Nexus is taking a bit to wake up. Please click '➤' again.")
        except Exception as e:
            st.error("Could not connect to Nexus. Check if Render is Live.")

        st.rerun()
