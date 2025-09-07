import streamlit as st
import requests

st.set_page_config(page_title="Iron Lady Chatbot", layout="centered")
st.title("🤖 Iron Lady FAQ Chatbot")

# Assign persistent user_id
if "user_id" not in st.session_state:
    st.session_state["user_id"] = "user_123"

# Maintain chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if user_input := st.chat_input("Ask about Iron Lady programs..."):
    # Show user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Call FastAPI backend
    response = requests.post(
        "http://127.0.0.1:8000/chat",
        json={"user_id": st.session_state["user_id"], "message": user_input}
    )
    bot_reply = response.json()["reply"]

    # Show bot reply
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    with st.chat_message("assistant"):
        st.markdown(bot_reply)
