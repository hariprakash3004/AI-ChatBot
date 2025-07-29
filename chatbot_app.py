import streamlit as st
from groq import Groq
import os
import time
from dotenv import load_dotenv

# -------------------------------
# Load API Key from .env file
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Check if key is found
if not GROQ_API_KEY:
    st.error("❌ GROQ_API_KEY not found. Please add it to your .env file.")
    st.stop()

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

# -------------------------------
# Custom Page Styling
st.set_page_config(page_title="💬 Groq AI Chatbot", layout="wide")

st.markdown("""
    <style>
        body {
            background-color: #f2f6ff;
        }
        .stChatMessage {
            padding: 1rem;
            border-radius: 10px;
            margin-bottom: 1rem;
        }
        .user {
            background-color: #e8f0fe;
            color: #000;
        }
        .assistant {
            background-color: #d1e7dd;
            color: #000;
        }
        footer {
            visibility: hidden;
        }
        .footer-text {
            position: fixed;
            bottom: 10px;
            left: 0;
            width: 100%;
            text-align: center;
            font-size: 14px;
            color: gray;
        }
    </style>
""", unsafe_allow_html=True)

# -------------------------------
# App Title
st.title("🤖 AI Chatbot")
st.caption("Chat with lightning-fast LLMs  LLaMA3 ⚡")

# -------------------------------
# Session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# -------------------------------
# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        bubble_class = "user" if msg["role"] == "user" else "assistant"
        st.markdown(f'<div class="stChatMessage {bubble_class}">{msg["content"]}</div>', unsafe_allow_html=True)

# -------------------------------
# Input box for new message
prompt = st.chat_input("💬 Ask me anything...")

if prompt:
    # Save user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(f'<div class="stChatMessage user">{prompt}</div>', unsafe_allow_html=True)

    # Assistant response placeholder
    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.markdown("⏳ Typing...")

        # Groq model call
        response = client.chat.completions.create(
            model="llama3-70b-8192",  
            messages=st.session_state.messages
        )
        reply = response.choices[0].message.content
        time.sleep(1)
        placeholder.markdown(f'<div class="stChatMessage assistant">{reply}</div>', unsafe_allow_html=True)

    # Save assistant message
    st.session_state.messages.append({"role": "assistant", "content": reply})

# -------------------------------
# Footer
st.markdown('<div class="footer-text">Built with ❤️ using Streamlit & Groq - By HARI PRAKASH</div>', unsafe_allow_html=True)
