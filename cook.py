import streamlit as st
import pandas as pd 
import time
from google import genai
from google.genai import types

def cook_food(prompt, client):
    if prompt:
        msg = st.toast("Gathering ingredients...")
        time.sleep(2)
        msg = st.toast("Cooking...")
        time.sleep(2)
        msg = st.toast("Ready!", icon="🥞")
        time.sleep(2)
        st.write(f"So you want to prepare {prompt} today.")
        time.sleep(1)
        st.write("Let's see how you can make it.")
        response = client.models.generate_content(
            model="gemini-2.0-flash", 
            contents=f"Write a detailed recipe for {prompt}")
        st.write(response.text)


if __name__=="__main__":
    API_KEY = "AIzaSyCCwpuFzmikkxtt2_AnJ9jjE-APzGJwrTI"
    client = genai.Client(api_key=API_KEY)
    st.title("Recipe Generator")
    prompt = st.chat_input("What's cooking?")
    cook_food(prompt, client)