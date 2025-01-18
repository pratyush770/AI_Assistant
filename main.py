import streamlit as st  # for ui generation
from chatbot import generate_prompt  # for generating prompt
from text_translator import translate_text  # for translating text
from code_assistant import code_assistant  # for code assistance
from grammar_check import grammar_check  # for grammar check
from exam_tutor import generate_question_and_answers  # for generating questions and answers

st.set_page_config(  # set page configurations
    page_title="AI Assistant",
    page_icon='🤖',
)

st.title("Your personalized AI Assistant 🤖")  # for giving title to the app
st.sidebar.title("Choose an option ✅")  # for giving sidebar title
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

if st.sidebar.button("Text translator"):  # for text translation
    if st.session_state.selected_option != "translate":
        reset_query()
    st.session_state.selected_option = "translate"

if st.sidebar.button("Code assistant"):
    if st.session_state.selected_option != "code_assistant":
        reset_query()
    st.session_state.selected_option = "code_assistant"

if st.sidebar.button("Grammar check"):
    if st.session_state.selected_option != "check":
        reset_query()
    st.session_state.selected_option = "check"

if st.sidebar.button("Exam tutor"):
    if st.session_state.selected_option != "tutor":
        reset_query()
    st.session_state.selected_option = "tutor"

# Handle the selected option
if st.session_state.selected_option == "chatbot":  # for chatbot
    st.write("")
    query = st.text_area("Ask me anything", height=300)  # ask for user input
    if query and query != st.session_state.query:  # check if input has changed
        st.session_state.query = query  # update session state
        with st.spinner("Generating response.."):
            response = generate_prompt(query)  # function call
            st.session_state.response = response  # save response
    if st.session_state.response:
        st.write(st.session_state.response)  # display response

if st.session_state.selected_option == "translate":  # for text translation
    st.write("")
    query = st.text_area("Enter text", height=300)  # ask for user input
    target_lang = st.selectbox(
        "Select a language",
        ("Select translation language",) + languages,
    )
    if query and target_lang != "Select translation language" and (
        query != st.session_state.query or target_lang != st.session_state.target_lang
    ):
        st.session_state.query = query
        st.session_state.target_lang = target_lang
        with st.spinner("Translating text..."):
            response = translate_text(query, target_lang)  # function call
            st.session_state.response = response  # save response
    if st.session_state.response:
        st.write(st.session_state.response)  # display response

if st.session_state.selected_option == "code_assistant":  # for code assistant
    st.write("")
    query = st.text_area("Enter your code snippet here", height=300)  # ask for user input
    query2 = st.text_input("Ask a question")
    if query and query2 and (
        query != st.session_state.query or query2 != st.session_state.query2
    ):
        st.session_state.query = query
        st.session_state.query2 = query2
        with st.spinner("Generating response.."):
            response = code_assistant(query, query2)  # function call
            st.session_state.response = response  # save response
    if st.session_state.response:
        st.write(st.session_state.response)  # display response

if st.session_state.selected_option == "check":  # for grammar check
    st.write("")
    query = st.text_area("Enter text to check for grammatical mistakes", height=300)  # ask for user input
    if query and query != st.session_state.query:
        st.session_state.query = query  # update session state
        with st.spinner("Generating response.."):
            response = grammar_check(query)  # function call
            st.session_state.response = response  # save response
    if st.session_state.response:
        st.write(st.session_state.response)  # display response

if st.session_state.selected_option == "tutor":  # for generating questions and answers
    st.write("")
    query = st.text_area("Enter text to generate questions", height=300)  # ask for user input
    if query and query != st.session_state.query:  # check if input has changed
        st.session_state.query = query  # update session state
        with st.spinner("Generating questions.."):
            response = generate_question_and_answers(query)  # function call
            st.session_state.response = response  # save response
    if st.session_state.response:
        formatted_response = response.replace("\n", "<br>")
        st.markdown(formatted_response, unsafe_allow_html=True)  # display formatted response with line breaks
