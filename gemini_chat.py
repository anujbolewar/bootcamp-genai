import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

st.title("🤖 Gemini Chatbot")
st.markdown("*Ask me anything!*")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("Type your question here...")

if user_input:
    with st.chat_message("user"):
        st.write(user_input)
    
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = model.generate_content(user_input)
            st.write(response.text)
    
    st.session_state.messages.append({"role": "assistant", "content": response.text})

if st.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()
