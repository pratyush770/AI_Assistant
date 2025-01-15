import streamlit as st
from chatbot import give_prompts
st.title("Your personalized AI Assistant 🤖")

st.sidebar.title("Choose a service")
st.sidebar.write("")
st.sidebar.write("")
st.sidebar.write("")
chatbot = st.sidebar.button("Chatbot")
doc_summ = st.sidebar.button("Document summarization")
translate = st.sidebar.button("Text translation")

if chatbot:
    st.write("")
    query = st.text_input("Ask me anything")
    if query:
        response = give_prompts(query)
        st.write(response)