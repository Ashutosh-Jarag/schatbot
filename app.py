import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai
from google.api_core.exceptions import GoogleAPIError

# --- 1. Configuration and Initialization ---

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    st.error("❌ GOOGLE_API_KEY not found. Please add it to your .env file.")
    st.stop()

try:
    genai.configure(api_key=API_KEY)
except Exception as e:
    st.error(f"❌ Error initializing Gemini Client: {e}")
    st.stop()

MODEL_NAME = "gemini-2.0-flash"

# --- 2. Streamlit Page Setup ---
st.set_page_config(page_title="Gemini Chatbot", layout="centered")

# --- 3. Custom CSS ---
st.markdown("""
<style>
    body {
        background: linear-gradient(135deg, #eef4ff 0%, #f9fbff 100%);
        font-family: 'Poppins', sans-serif;
    }

    /* Fixed Header */
    .fixed-header {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        background: linear-gradient(90deg, #0072ff, #00c6ff);
        color: white;
        text-align: center;
        font-size: 1.5rem;
        font-weight: 600;
        padding: 1rem 0;
        z-index: 999;
        box-shadow: 0 2px 12px rgba(0,0,0,0.1);
    }

    /* Chat layout */
    .chat-wrapper {
        margin-top: 100px;
        margin-bottom: 80px;
        display: flex;
        flex-direction: column;
        gap: 10px;
    }

    /* Message styles */
    .message-container {
        display: flex;
        align-items: flex-start;
        gap: 10px;
        padding: 0 1rem;
    }

    /* Assistant (Gemini) */
    .assistant {
        justify-content: flex-start;
    }
    .assistant-bubble {
        background: #f3f4f6;
        color: #111;
        border-radius: 15px 15px 15px 2px;
        padding: 0.8rem 1rem;
        max-width: 75%;
        word-wrap: break-word;
    }

    /* User */
    .user {
        justify-content: flex-end;
    }
    .user-bubble {
        background: #0072ff;
        color: white;
        border-radius: 15px 15px 2px 15px;
        padding: 0.8rem 1rem;
        max-width: 75%;
        word-wrap: break-word;
    }

    /* Labels */
    .sender-label {
        font-size: 0.8rem;
        margin-bottom: 3px;
        color: #666;
    }

    .sender-label.user {
        text-align: right;
        margin-right: 10px;
    }

    .sender-label.assistant {
        text-align: left;
        margin-left: 10px;
    }

    /* Refresh Button */
    .refresh-btn {
        position: fixed;
        top: 18px;
        right: 25px;
        background-color: white;
        color: #0072ff;
        border: 2px solid white;
        border-radius: 8px;
        padding: 4px 10px;
        font-weight: 600;
        font-size: 0.9rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        cursor: pointer;
    }

    .refresh-btn:hover {
        background-color: #0072ff;
        color: white;
    }

    .stChatInput textarea {
        border-radius: 10px !important;
        border: 1px solid #0072ff !important;
    }
</style>
""", unsafe_allow_html=True)

# --- Fixed Header with Refresh ---
st.markdown("""
<div class="fixed-header">
    🤖 Gemini Chatbot
    <button class="refresh-btn" onClick="window.location.reload()">🔄 Refresh</button>
</div>
""", unsafe_allow_html=True)

# --- 4. Sidebar Configuration ---
st.sidebar.header("⚙️ Chatbot Settings")
st.sidebar.info(f"Using Model: **{MODEL_NAME}**")

DEFAULT_INSTRUCTION = (
    "You are a helpful AI assistant that provides concise and relevant answers."
)

new_instruction = st.sidebar.text_area(
    "Edit Chatbot Persona (System Instruction):",
    value=DEFAULT_INSTRUCTION,
    height=200
)

# Reset chat manually
if st.sidebar.button("✨ Apply Changes & Reset Chat"):
    st.session_state["messages"] = []
    st.session_state["system_instruction"] = new_instruction
    st.rerun()

# --- 5. Session Management ---
if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "system_instruction" not in st.session_state:
    st.session_state["system_instruction"] = new_instruction

model = genai.GenerativeModel(MODEL_NAME)

# --- 6. Display Chat History ---
st.markdown('<div class="chat-wrapper">', unsafe_allow_html=True)

for msg in st.session_state["messages"]:
    if msg["role"] == "user":
        st.markdown(f"<div class='sender-label user'>👤 You</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='message-container user'><div class='user-bubble'>{msg['content']}</div></div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='sender-label assistant'>🤖 Gemini</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='message-container assistant'><div class='assistant-bubble'>{msg['content']}</div></div>", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# --- 7. Handle New User Input ---
if prompt := st.chat_input("Type your question here..."):
    st.session_state["messages"].append({"role": "user", "content": prompt})
    st.markdown(f"<div class='sender-label user'>👤 You</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='message-container user'><div class='user-bubble'>{prompt}</div></div>", unsafe_allow_html=True)

    try:
        with st.spinner("🤖 Thinking..."):
            response_stream = model.generate_content(
                [st.session_state["system_instruction"], prompt],
                stream=True
            )
            full_response = ""
            for chunk in response_stream:
                if chunk.candidates and chunk.candidates[0].content.parts:
                    part = chunk.candidates[0].content.parts[0].text
                    full_response += part.strip().replace("\n", " ")

        st.markdown(f"<div class='sender-label assistant'>🤖 Gemini</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='message-container assistant'><div class='assistant-bubble'>{full_response}</div></div>", unsafe_allow_html=True)

        st.session_state["messages"].append({"role": "assistant", "content": full_response})

    except GoogleAPIError as e:
        st.error(f"❌ API Error: {e}")
    except Exception as e:
        st.error(f"❌ Unexpected Error: {e}")
