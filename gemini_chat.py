import streamlit as st
import google.generativeai as genai

# Your Gemini API Key
API_KEY = "AIzaSyCIJjV6wVstDJkjkNzN4t2tpzs1tnLZGiw"

# Setup Gemini
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

# Page title
st.title("🤖 Gemini Chatbot")
st.markdown("*Ask me anything!*")

# Create chat history (stores all messages)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show all previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Get user input
user_input = st.chat_input("Type your question here...")

if user_input:
    # Show user message
    with st.chat_message("user"):
        st.write(user_input)
    
    # Save user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = model.generate_content(user_input)
            st.write(response.text)
    
    # Save AI response
    st.session_state.messages.append({"role": "assistant", "content": response.text})

# Clear chat button
if st.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()
