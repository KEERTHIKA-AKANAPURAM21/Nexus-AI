import streamlit as st
from groq import Groq

# 1. INITIALIZATION
st.set_page_config(page_title="Nexus AI", layout="wide")

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error("GROQ_API_KEY missing in Streamlit Secrets!")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hi! Nexus is ready. How can I help you today?"}]

# 2. STYLING (Hides Streamlit clutter and styles the chat)
st.markdown("""
    <style>
    div[data-testid="stToolbar"], div[data-testid="stStatusWidget"] {display: none !important;}
    footer {visibility: hidden;}
    .stChatMessage {background-color: #f0f2f6 !important; border-radius: 10px; padding: 10px; margin-bottom: 10px;}
    
    /* This makes the popover look like a small plus button */
    button[data-testid="baseButton-secondary"] {
        border-radius: 50% !important;
        width: 40px !important;
        height: 40px !important;
        padding: 0px !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Nexus AI")

# 3. DISPLAY CHAT HISTORY
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 4. BOTTOM INPUT AREA (The ChatGPT Look)
# We create two columns: a small one for the (+) and a big one for the input
col1, col2 = st.columns([0.05, 0.95], vertical_alignment="bottom")

with col1:
    # This is your "Plus" button menu
    with st.popover("➕"):
        st.markdown("### Attach")
        uploaded_file = st.file_uploader("Upload files", type=['pdf', 'txt', 'docx'], label_visibility="collapsed")
        if st.button("🔗 Add from Google Drive"):
            st.warning("Google Drive integration requires API setup. Use 'Upload' for now.")
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = [{"role": "assistant", "content": "Chat cleared!"}]
            st.rerun()

with col2:
    prompt = st.chat_input("Ask Nexus...")

# 5. LOGIC
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    try:
        with st.spinner("Nexus is thinking..."):
            context = f"(Attached: {uploaded_file.name}) " if uploaded_file else ""
            
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": context + prompt}]
            )
            ans = completion.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": ans})
            with st.chat_message("assistant"):
                st.write(ans)
    except Exception as e:
        st.error(f"Error: {e}")
