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
    st.session_state.messages = [{"role": "assistant", "content": "Hi! Nexus (Groq Edition) is ready. How can I help?"}]

# 2. STYLING (Kept your professional look)
st.markdown("""
    <style>
    div[data-testid="stToolbar"], div[data-testid="stStatusWidget"] {display: none !important;}
    footer {visibility: hidden;}
    .stChatMessage {background-color: #f0f2f6 !important; border-radius: 10px; padding: 10px; margin-bottom: 10px;}
    .stChatMessage p {color: #1E1E1E !important;}
    </style>
""", unsafe_allow_html=True)

st.title("Nexus AI")

# 3. DISPLAY CHAT
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 4. INPUT AREA
prompt = st.chat_input("Ask Nexus...")

# 5. LOGIC
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    try:
        with st.spinner("Nexus is thinking..."):
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}]
            )
            ans = completion.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": ans})
            with st.chat_message("assistant"):
                st.write(ans)
    except Exception as e:
        st.error(f"Error: {e}")
