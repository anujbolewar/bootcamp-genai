import streamlit as st
import requests
import json
import time

def generate_ruskin_bond_story(theme):
    """Generate a Ruskin Bond inspired story using Ollama"""
    if theme:
        msg = st.toast("Gathering memories from the hills...")
        time.sleep(1)
        msg = st.toast("Crafting a nostalgic tale...")
        
        st.write(f"**Theme:** {theme}")
        st.write("---")
        
        # Call Ollama API with Ruskin Bond style prompt
        url = "http://localhost:11434/api/generate"
        
        prompt = f"""Write a short story inspired by Ruskin Bond's writing style about: {theme}

The story should have these characteristics:
- Simple, elegant prose
- Set in the hills or mountains of India
- Nostalgic and warm tone
- Focus on nature, childhood memories, or simple village life
- Observations about people, animals, or landscapes
- Gentle humor and wisdom
- Around 200-300 words

Write the complete story:"""
        
        payload = {
            "model": "tinyllama",
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.8,
                "top_p": 0.9
            }
        }
        
        try:
            with st.spinner("🏔️ Writing from the hills..."):
                response = requests.post(url, json=payload, timeout=60)
                if response.status_code == 200:
                    result = response.json()
                    st.toast("Story ready!", icon="📖")
                    st.markdown("### ✍️ A Tale from the Hills")
                    st.write(result['response'])
                else:
                    st.error(f"Error: {response.status_code}")
        except Exception as e:
            st.error(f"Connection error: {e}")

def main():
    st.title("📖 Ruskin Bond Story Generator")
    st.markdown("*Create stories inspired by the master storyteller of the hills*")
    st.markdown("*Powered by Ollama (TinyLlama)*")
    
    st.write("---")
    
    # Story theme options
    st.subheader("Choose a theme or write your own:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🌳 A Tree", use_container_width=True):
            st.session_state.theme = "an old tree in the mountains"
    
    with col2:
        if st.button("🦜 A Bird", use_container_width=True):
            st.session_state.theme = "a bird in the garden"
    
    with col3:
        if st.button("🌧️ The Rain", use_container_width=True):
            st.session_state.theme = "monsoon in the hills"
    
    col4, col5, col6 = st.columns(3)
    
    with col4:
        if st.button("👦 Childhood", use_container_width=True):
            st.session_state.theme = "childhood memories in a hill station"
    
    with col5:
        if st.button("🏘️ Village Life", use_container_width=True):
            st.session_state.theme = "life in a small mountain village"
    
    with col6:
        if st.button("🌄 Mountains", use_container_width=True):
            st.session_state.theme = "the Himalayan mountains"
    
    st.write("---")
    
    # Custom theme input
    custom_theme = st.text_input("Or enter your own theme:", 
                                 placeholder="e.g., an old man and his garden")
    
    if st.button("✨ Generate Story", type="primary"):
        theme_to_use = custom_theme if custom_theme else st.session_state.get('theme', '')
        if theme_to_use:
            generate_ruskin_bond_story(theme_to_use)
        else:
            st.warning("Please select a theme or enter your own!")
    
    # Initialize session state
    if 'theme' not in st.session_state:
        st.session_state.theme = ""

if __name__ == "__main__":
    main()
