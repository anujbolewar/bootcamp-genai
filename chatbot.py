import streamlit as st
import requests
import json

def chat_with_ollama(message, chat_history):
    """Send message to Ollama and get response"""
    url = "http://localhost:11434/api/generate"
    
    # Build context from chat history
    context = ""
    for msg in chat_history:
        context += f"{msg['role']}: {msg['content']}\n"
    
    prompt = f"{context}user: {message}\nassistant:"
    
    payload = {
        "model": "tinyllama",
        "prompt": prompt,
        "stream": False
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            result = response.json()
            return result['response']
        else:
            return f"Error: {response.status_code}"
    except Exception as e:
        return f"Connection error: {e}"

def main():
    st.title("🤖 AI Chatbot")
    st.markdown("*Powered by Ollama (TinyLlama)*")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask me anything..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get bot response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = chat_with_ollama(prompt, st.session_state.messages)
                st.markdown(response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Clear chat button
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

if __name__ == "__main__":
    main()
