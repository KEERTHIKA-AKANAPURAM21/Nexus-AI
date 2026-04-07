import streamlit as st
from groq import Groq

# 1. INITIALIZATION
st.set_page_config(page_title="Nexus AI", layout="wide")

# Link to the Secret you just saved
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error("GROQ_API_KEY missing in Streamlit Secrets!")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hi! Nexus is ready. How can I help you today?"}]

# 2. STYLING (Professional look)
st.markdown("""
    <style>
    div[data-testid="stToolbar"], div[data-testid="stStatusWidget"] {display: none !important;}
    footer {visibility: hidden;}
    .stChatMessage {background-color: #f0f2f6 !important; border-radius: 10px; padding: 10px; margin-bottom: 10px;}
    .stChatMessage p {color: #1E1E1E !important;}
    </style>
""", unsafe_allow_html=True)

# 3. SIDEBAR (The "Plus" Section)
with st.sidebar:
    st.title("📂 Nexus Attachments")
    st.info("Upload documents here to reference them in your chat.")
    
    # This acts as your 'Plus icon' menu
    uploaded_file = st.file_uploader("Add files", type=['pdf', 'txt', 'docx'])
    
    if uploaded_file:
        st.success(f"Successfully attached: {uploaded_file.name}")
    
    st.divider()
    if st.button("Clear Conversation"):
        st.session_state.messages = [{"role": "assistant", "content": "Conversation cleared. How can I help?"}]
        st.rerun()

# 4. MAIN INTERFACE
st.title("Nexus AI")

# DISPLAY CHAT
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# INPUT AREA
prompt = st.chat_input("Ask Nexus...")

# 5. LOGIC
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    try:
        with st.spinner("Nexus is thinking..."):
            # If a file is uploaded, we can tell the AI about it
            context = ""
            if uploaded_file:
                context = f"(User has attached a file named {uploaded_file.name}) "

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
