import os
import streamlit as st
from groq import Groq

# Read API key from Streamlit secrets
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY")

st.set_page_config(page_title="Simple Chatbot", page_icon="🤖")
st.title("🤖 Simple Groq Chatbot")

if not GROQ_API_KEY:
    st.error("GROQ_API_KEY not found. Add it to .streamlit/secrets.toml")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

# Chat memory
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

# Show chat history
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

# User input
user_input = st.chat_input("Ask something...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.write(user_input)

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=st.session_state.messages,
        temperature=0.7,
        max_tokens=300
    )

    reply = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": reply})

    with st.chat_message("assistant"):
        st.write(reply)
