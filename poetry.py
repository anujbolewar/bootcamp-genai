import streamlit as st
import time
import requests
import json

def generate_poetry(topic):
    if topic:
        msg = st.toast("Gathering inspiration...")
        time.sleep(1)
        msg = st.toast("Crafting verses...")
        
        st.write(f"**Your theme:** {topic}")
        st.write("---")
        
        # Call Ollama API
        url = "http://localhost:11434/api/generate"
        payload = {
            "model": "tinyllama",
            "prompt": f"Write a beautiful poem about {topic}. Make it emotional and vivid.",
            "stream": False
        }
        
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                result = response.json()
                st.toast("Poetry ready!", icon="✨")
                st.write(result['response'])
            else:
                st.error(f"Error: {response.status_code}")
        except Exception as e:
            st.error(f"Connection error: {e}")

if __name__=="__main__":
    st.title("✨ Poetry Generator")
    st.markdown("Enter a theme and let AI create a poem for you")
    st.markdown("*Powered by Ollama (TinyLlama)*")
    topic = st.chat_input("What should I write about?")
    generate_poetry(topic)
