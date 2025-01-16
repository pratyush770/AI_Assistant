import streamlit as st  # for ui generation
from chatbot import generate_prompt  # for generating prompt
from text_translator import translate_text  # for translating text
from code_assistant import code_assistant  # for code assistance

st.title("Your personalized AI Assistant 🤖")  # for giving title to the app
st.sidebar.title("Choose an option ⚙️")  # for giving sidebar title
st.sidebar.write("")  # empty line
st.sidebar.write("")
st.sidebar.write("")

languages = (  # tuple of languages
    "Afrikaans", "Albanian", "Amharic", "Arabic", "Armenian", "Azerbaijani", "Basque", "Belarusian", "Bengali", "Bosnian", "Bulgarian", "Catalan",
    "Cebuano", "Chichewa", "Chinese (Simplified)", "Chinese (Traditional)", "Corsican", "Croatian", "Czech", "Danish", "Dutch", "English", "Esperanto",
    "Estonian", "Filipino", "Finnish", "French", "Frisian", "Galician", "Georgian", "German", "Greek", "Gujarati", "Haitian Creole", "Hausa",
    "Hawaiian", "Hebrew", "Hindi", "Hmong", "Hungarian", "Icelandic", "Igbo", "Indonesian", "Irish", "Italian", "Japanese", "Javanese", "Kannada",
    "Kazakh", "Khmer", "Kinyarwanda", "Korean", "Kurdish (Kurmanji)", "Kyrgyz", "Lao", "Latin", "Latvian", "Lithuanian", "Luxembourgish",
    "Macedonian", "Malagasy", "Malay", "Malayalam", "Maltese", "Maori", "Marathi", "Mongolian", "Myanmar (Burmese)", "Nepali", "Norwegian",
    "Odia (Oriya)", "Pashto", "Persian", "Polish", "Portuguese", "Punjabi", "Romanian", "Russian", "Samoan", "Scots Gaelic", "Serbian", "Sesotho",
    "Shona", "Sindhi", "Sinhala", "Slovak", "Slovenian", "Somali", "Spanish", "Sundanese", "Swahili", "Swedish", "Tajik", "Tamil", "Tatar", "Telugu",
    "Thai", "Turkish", "Turkmen", "Ukrainian", "Urdu", "Uyghur", "Uzbek", "Vietnamese", "Welsh", "Xhosa", "Yiddish", "Yoruba", "Zulu"
)

# Initialize session state for selected option and query/response
if "selected_option" not in st.session_state:
    st.session_state.selected_option = None
if "query" not in st.session_state:
    st.session_state.query = ""  # default state
if "query2" not in st.session_state:
    st.session_state.query2 = ""  # default state
if "target_lang" not in st.session_state:
    st.session_state.target_lang = ""
if "response" not in st.session_state:
    st.session_state.response = ""


def reset_query():  # Function to reset the queries and response when switching options
    st.session_state.query = ""
    st.session_state.query2 = ""
    st.session_state.response = ""


# Sidebar buttons to select options
if st.sidebar.button("Chatbot"):  # for chatbot
    if st.session_state.selected_option != "chatbot":
        reset_query()
    st.session_state.selected_option = "chatbot"

if st.sidebar.button("Text translation"):  # for text translation
    if st.session_state.selected_option != "translate":
        reset_query()
    st.session_state.selected_option = "translate"

if st.sidebar.button("Code assistant"):
    if st.session_state.selected_option != "code_assistant":
        reset_query()
    st.session_state.selected_option = "code_assistant"

if st.sidebar.button("Document summarization"):
    if st.session_state.selected_option != "doc_summ":
        reset_query()
    st.session_state.selected_option = "doc_summ"

# Handle the selected option
if st.session_state.selected_option == "chatbot":  # for chatbot
    st.write("")
    query = st.text_input("Ask me anything", value=st.session_state.query)  # asks user for input
    with st.spinner("Generating response.."):  # shows a spinner while generating a response
        if query:
            st.session_state.query = query  # save the input in session state
            response = generate_prompt(query)  # function call
            st.session_state.response = response  # save the response in session state
            st.write(response)
        elif st.session_state.response:
            st.write(st.session_state.response)  # display the previous response if available

if st.session_state.selected_option == "translate":  # for text translation
    st.write("")
    query = st.text_input("Enter text", value=st.session_state.query)  # ask user input
    # Dropdown for selecting target language with a placeholder
    target_lang = st.selectbox(
        "Select a language",
        ("Select translation language",) + languages,  # Add a placeholder option
    )
    # Only proceed if a valid language is selected and text is entered
    if query and target_lang != "Select translation language":
        # Update session state for query and target language
        if query != st.session_state.query or target_lang != st.session_state.target_lang:
            st.session_state.query = query
            st.session_state.target_lang = target_lang
            with st.spinner("Translating text..."):  # perform translation
                response = translate_text(query, target_lang)  # function call
                st.session_state.response = response  # save the response in session state
    else:
        response = st.session_state.response  # retrieve the response from session state
    if response:
        st.write(response)  # display the response

if st.session_state.selected_option == "code_assistant":  # for code assistant
    st.write("")
    query = st.text_area("Enter your code snippet here", value=st.session_state.query, height=250)  # asks user for input
    query2 = st.text_input("Ask a question", value=st.session_state.query2)  # asks user for input
    with st.spinner("Generating response.."):  # shows a spinner while generating a response
        if query and query2:
            st.session_state.query = query  # save the input in session state
            st.session_state.query2 = query2
            response = code_assistant(query, query2)  # function call
            st.session_state.response = response  # save the response in session state
            st.write(response)
        elif st.session_state.response:
            st.write(st.session_state.response)  # display the previous response if available

