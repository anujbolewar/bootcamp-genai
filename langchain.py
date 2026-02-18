import streamlit as st
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI assistant."),
    ("user", "Question: {question}")
])

st.title("Langchain Demo with TinyLlama")
input_text = st.text_input("Your question: ")

model = Ollama(model="tinyllama")

output_parser = StrOutputParser()

chain = prompt | model | output_parser

if input_text:
    response = chain.invoke({"question": input_text})
    st.write(response)