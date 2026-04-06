import streamlit as st
import google.generativeai as genai

# 1. INITIALIZATION & LAYOUT
st.set_page_config(page_title="Nexus AI", layout="wide")

# Configure Gemini directly using Streamlit Secrets
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("API Key missing or invalid in Streamlit Secrets. Please check your dashboard.")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi there, how can I assist you today?"}
    ]

# 2. CUSTOM STYLING - Clean Interface
st.markdown("""
    <style>
    /* HIDE GITHUB ICON & TOOLBAR */
    div[data-testid="stToolbar"] {
        display: none !important;
    }

    /* HIDE MANAGE APP BUTTON */
    div[data-testid="stStatusWidget"] {
        display: none !important;
    }
    
    header[data-testid="stHeader"] {
        visibility: visible !important;
        background-color: rgba(255, 255, 255, 0); 
    }

    /* Chat visibility fixes */
    .stChatMessage {
        background-color: #f0f2f6 !important;
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 10px;
    }
    .stChatMessage p {
        color: #1E1E1E !important; 
    }

    /* Style the Plus Button and Hide Footer */
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
            
    with c2:
        prompt = st.text_input("Ask Nexus", key="user_prompt", label_visibility="collapsed", placeholder="Ask Nexus...")

    with c3:
        st.selectbox("Mode", ["Fast ▾", "Quality"], label_visibility="collapsed", key="mode")

    with c4:
        send_btn = st.button("➤")

# 5. LOGIC: HANDLING THE MESSAGE DIRECTLY WITH GEMINI
if (send_btn or prompt) and prompt:
    # Check for duplicate sends
    if "last_sent" not in st.session_state or st.session_state.last_sent != prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.last_sent = prompt 
        
        try:
            with st.spinner("Nexus is thinking..."):
                # Call Gemini API directly
                response = model.generate_content(prompt)
                ans = response.text
                
                # Append the AI response to session state
                st.session_state.messages.append({"role": "assistant", "content": ans})
                
        except Exception as e:
            st.error(f"Nexus encountered an error: {e}")

        st.rerun()
