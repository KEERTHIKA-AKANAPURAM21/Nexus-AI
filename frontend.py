import streamlit as st
from groq import Groq
import pypdf

# 1. INITIALIZATION & CONFIG
st.set_page_config(page_title="Nexus AI", layout="wide")

# Function to extract text from different file types
def extract_text_from_file(file):
    try:
        if file.type == "text/plain":
            return file.read().decode("utf-8")
        elif file.type == "application/pdf":
            pdf_reader = pypdf.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                content = page.extract_text()
                if content:
                    text += content
            return text
        else:
            return "Unsupported file type."
    except Exception as e:
        return f"Error reading file: {str(e)}"

# Secure Client Connection
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error("GROQ_API_KEY missing in Streamlit Secrets!")

# Session State for Chat History
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hi! Nexus is ready. How can I help you today?"}]

# 2. STYLING
st.markdown("""
    <style>
    div[data-testid="stToolbar"], div[data-testid="stStatusWidget"] {display: none !important;}
    footer {visibility: hidden;}
    .stChatMessage {background-color: #f0f2f6 !important; border-radius: 10px; padding: 10px; margin-bottom: 10px;}
    
    /* Plus Button Style */
    button[data-testid="baseButton-secondary"] {
        border-radius: 50% !important;
        width: 35px !important;
        height: 35px !important;
        padding: 0px !important;
    }

    /* Column Alignment */
    div[data-testid="column"] {
        display: flex;
        align-items: flex-end;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Nexus AI")

# 3. DISPLAY CHAT HISTORY
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 4. BOTTOM INPUT AREA
col1, col2, col3 = st.columns([0.05, 0.12, 0.83], vertical_alignment="bottom")

with col1:
    with st.popover("➕"):
        st.markdown("### Attach Content")
        
        # Option 1: Local Upload
        uploaded_file = st.file_uploader("Upload local files", type=['pdf', 'txt'], label_visibility="visible")
        
        st.divider()
        
        # Option 2: Google Drive Placeholder
        if st.button("📁 Add from Google Drive"):
            st.info("Google Drive Integration: Cloud Project & OAuth setup required for live access.")
            
        # Option 3: Clear Chat
        if st.button("🗑️ Reset Conversation"):
            st.session_state.messages = [{"role": "assistant", "content": "Chat cleared!"}]
            st.rerun()

with col2:
    if st.button("🔄 New Chat"):
        st.session_state.messages = [{"role": "assistant", "content": "New session started."}]
        st.rerun()

with col3:
    # Badge to show what is currently "in memory"
    if uploaded_file:
        st.markdown(f"📎 **Attached:** `{uploaded_file.name}`")
    prompt = st.chat_input("Ask Nexus...")

# 5. PROCESSING LOGIC
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    try:
        with st.spinner("Nexus is processing..."):
            file_context = ""
            if uploaded_file:
                content = extract_text_from_file(uploaded_file)
                file_context = f"\n[REFERENCE DOCUMENT: {content}]\n"
            
            final_content = f"{file_context} User Question: {prompt}"

            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": final_content}]
            )
            
            ans = completion.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": ans})
            with st.chat_message("assistant"):
                st.write(ans)
                
    except Exception as e:
        st.error(f"Error: {e}")
