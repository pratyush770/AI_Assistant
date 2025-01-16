import streamlit as st
from chatbot import generate_prompt  # for generating prompt
from text_translator import translate_text

st.title("Your personalized AI Assistant 🤖")  # for giving title to the app
st.sidebar.title("Choose an option ⚙️")  # for giving sidebar title
st.sidebar.write("")  # empty line
st.sidebar.write("")
st.sidebar.write("")

# Initialize session state for selected option and query/response
if "selected_option" not in st.session_state:
    st.session_state.selected_option = None
if "query" not in st.session_state:
    st.session_state.query = ""
if "lang1" not in st.session_state:
    st.session_state.lang1 = "Hindi"  # default state
if "response" not in st.session_state:
    st.session_state.response = ""

# Sidebar buttons to select options
if st.sidebar.button("Chatbot"):  # for chatbot
    st.session_state.selected_option = "chatbot"
if st.sidebar.button("Document summarization"):
    st.session_state.selected_option = "doc_summ"
if st.sidebar.button("Text translation"):
    st.session_state.selected_option = "translate"

# Handle the selected option
if st.session_state.selected_option == "chatbot":  # for chatbot
    st.write("")
    query = st.text_input("Ask me anything", value=st.session_state.query)  # asks user for input
    with st.spinner("Generating response"):  # shows a spinner while generating a response
        if query:
            st.session_state.query = query  # save the input in session state
            response = generate_prompt(query)  # function call
            st.session_state.response = response  # save the response in session state
            st.write(response)
        elif st.session_state.response:
            st.write(st.session_state.response)  # display the previous response if available

if st.session_state.selected_option == "translate":  # for text translation
    st.write("")
    query = st.text_input("Enter text", value=st.session_state.query)  # asks user for input
    lang1 = st.selectbox("Select translation language", ("English", "Hindi", "Japanese"),
                         index=["English", "Hindi", "Japanese"].index(st.session_state.lang1))
    st.session_state.lang1 = lang1
    with st.spinner("Generating response"):  # shows a spinner while generating a response
        if query:
            st.session_state.query = query  # save the input in session state
            response = translate_text(query, lang1)  # function call
            st.session_state.response = response  # save the response in session state
            st.write(response.strip())

