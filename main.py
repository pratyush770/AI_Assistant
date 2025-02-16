import streamlit as st  # for ui generation
from chatbot import generate_prompt  # for generating prompt
from text_translator import translate_text  # for translating text
from code_assistant import code_assistant  # for code assistance
from exam_tutor import generate_question_and_answers  # for generating questions and answers
from grammar_check import grammar_check  # for grammar check
from langchain_core.messages import AIMessage, HumanMessage
import time

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
if "target_lang" not in st.session_state:
    st.session_state.target_lang = ""
if "response" not in st.session_state:
    st.session_state.response = ""


def reset_query():  # Function to reset the queries and response when switching options
    st.session_state.query = ""
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

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        AIMessage(content="Hello, how can i help you?")
    ]

# Handle the selected option
if st.session_state.selected_option == "chatbot":  # for chatbot
    st.write("")
    for message in st.session_state.chat_history:   # display chat history
        if isinstance(message, AIMessage):
            with st.chat_message("AI"):
                st.markdown(message.content)
        elif isinstance(message, HumanMessage):
            with st.chat_message("Human"):
                st.markdown(message.content)
    query = st.chat_input("Ask me anything")  # ask for user input
    if query and query.strip() != "":  # check if the input is valid
        st.session_state.chat_history.append(HumanMessage(content=query))
        with st.chat_message("Human"):
            st.markdown(query)  # display human message
        with st.chat_message("AI"):
            response = generate_prompt(query)  # generate response
            st.session_state.chat_history.append(AIMessage(content=response))
            message_placeholder = st.empty()  # create a placeholder for dynamic updates
            if "```" in response:
                time.sleep(0.1)   # delay of 1 second
                message_placeholder.empty()  # clear placeholder
                code_blocks = response.split("```")  # extract code blocks
                for i, block in enumerate(code_blocks):
                    block = block.strip()
                    if i % 2 == 1:  # code blocks (odd indices)
                        st.code(block)
                    elif block:  # normal text (even indices)
                        message_placeholder.write(block)
            else:
                displayed_text = ""  # word-by-word rendering
                for word in response.split():
                    displayed_text += word + " "
                    message_placeholder.write(displayed_text)  # updates the text dynamically
                    time.sleep(0.1)  # delay to create a typing effect

if st.session_state.selected_option == "translate":  # for text translation
    st.write("")
    query = st.text_input("Enter text")  # ask for user input
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
    if query and query != st.session_state.query:
        st.session_state.query = query
        with st.spinner("Generating response.."):
            response = code_assistant(query)  # function call
            st.session_state.response = response  # save response
    if st.session_state.response:
        st.write(st.session_state.response)  # display response

if st.session_state.selected_option == "check":  # for grammar check
    st.write("")
    query = st.text_input("Enter text to check for grammatical mistakes")  # ask for user input
    if query and query != st.session_state.query:
        st.session_state.query = query  # update session state
        with st.spinner("Generating response.."):
            response = grammar_check(query)  # function call
            st.session_state.response = response  # save response
    if st.session_state.response:
        st.write(st.session_state.response)  # display response

if st.session_state.selected_option == "tutor":  # for generating questions and answers
    st.write("")
    query = st.text_input("Enter text to generate questions")  # ask for user input
    if query and query != st.session_state.query:  # check if input has changed
        st.session_state.query = query  # update session state
        with st.spinner("Generating questions.."):
            response = generate_question_and_answers(query)  # function call
            st.session_state.response = response  # save response
    if st.session_state.response:
        formatted_response = response.replace("\n", "<br>")
        st.markdown(formatted_response, unsafe_allow_html=True)  # display formatted response with line breaks
