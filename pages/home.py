import streamlit as st  # for ui generation
from functions.chatbot import get_result  # for generating prompt
from functions.text_translator import translate_text  # for translating text
from functions.code_assistant import code_assistor  # for code assistance
from functions.exam_tutor import get_answers  # for generating questions and answers
from functions.grammar_check import grammar_check  # for grammar check
from functions.web_crawler import get_embeddings, get_vector_store, is_vector_store_initialized, initialize_vector_store, query_vector_store
from functions.pdf_crawler import get_embeddings_pdf, get_vector_store_pdf, is_vector_store_initialized_pdf, initialize_vector_store_pdf, query_vector_store_pdf
from langchain_core.messages import AIMessage, HumanMessage
from pypdf import PdfReader

st.set_page_config(  # set page configuration
    page_title="AI Assistant",
    page_icon='🤖',
)

st.title("Your personalized AI Assistant 🤖")  # for giving title to the app
st.sidebar.title("Choose an option ✅")  # for giving sidebar title
st.sidebar.write("")  # empty line
st.sidebar.write("")
st.sidebar.write("")

languages = (
    "Arabic", "Chinese", "Czeck", "Danish", "Dutch", "English", "French", "German",
    "Greek", "Hindi", "Hungarian", "Indonesian", "Italian", "Japanese", "Korean", "Marathi",
    "Polish", "Portuguese", "Russian", "Spanish", "Turkish"
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

if st.sidebar.button("Q&A tool"):
    if st.session_state.selected_option != "q&a_tool":
        reset_query()
    st.session_state.selected_option = "q&a_tool"

st.sidebar.divider()

if st.sidebar.button("Logout", type="tertiary"):
    st.switch_page("login.py")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        AIMessage(content="Hello, how can i help you?")
    ]


# handle the selected option
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
        # generate the AI response using the chat history
        response, updated_chat_history = get_result(query, st.session_state.chat_history[-3:])
        ai_response = AIMessage(content=response)
        st.session_state.chat_history.append(ai_response)
        # display the AI message
        with st.chat_message("AI"):
            st.markdown(response)

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
            response = code_assistor(query)  # function call
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
            response = get_answers(query)  # function call
            st.session_state.response = response  # save response
    if st.session_state.response:
        formatted_response = response.replace("\n", "<br>")
        st.markdown(f'<div style="font-size: 16px;">{formatted_response}</div>', unsafe_allow_html=True)

if st.session_state.selected_option == "q&a_tool":  # for q&a using rag
    st.write("")
    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
    with col1:
        website_clicked = st.button("Website")  # for website
    with col2:
        pdf_clicked = st.button("PDF file")  # for pdf
    # track button states using session state
    if website_clicked:
        st.session_state.website_clicked = True
        st.session_state.pdf_clicked = False
    elif pdf_clicked:
        st.session_state.pdf_clicked = True
        st.session_state.website_clicked = False

    # handle website option
    if getattr(st.session_state, "website_clicked", False):
        url = st.text_input("Enter the URL of the webpage:")  # ask for user input
        # reset query and response if the url changes
        if "current_url" not in st.session_state:
            st.session_state.current_url = None
        if url != st.session_state.current_url:
            st.session_state.query = ""  # reset query
            st.session_state.response = ""  # reset response
            st.session_state.current_url = url  # update current url
        try:
            if url:
                with st.spinner("Generating embeddings"):
                    _embeddings = get_embeddings()  # get centralized embeddings
                vector_store = get_vector_store(_embeddings)  # get centralized vector store
                # check if the vector store is already initialized
                if not is_vector_store_initialized(vector_store, url):
                    with st.spinner("Initializing vector"):
                        vector_store = initialize_vector_store(url, vector_store)
                else:
                    pass
                query = st.text_input("Enter your query:")  # ask for user input
                if query:
                    with st.spinner("Generating response"):
                        result = query_vector_store(vector_store, query, url)
                        st.write(result)
        except Exception as e:
            st.error(f"An error occurred: {e}")

    # handle pdf option
    elif getattr(st.session_state, "pdf_clicked", False):
        pdf_file = st.file_uploader("Upload PDF", type="pdf", accept_multiple_files=False)  # asks user to upload pdf file
        # track the current pdf file using session state
        if "current_pdf" not in st.session_state:
            st.session_state.current_pdf = None
        # reset query and response if a new pdf is uploaded
        if pdf_file and pdf_file.name != st.session_state.current_pdf:
            st.session_state.query = ""  # reset query
            st.session_state.response = ""  # reset response
            st.session_state.current_pdf = pdf_file.name  # update current pdf file name
        if pdf_file:
            try:
                # extract text from the uploaded pdf
                pdf_reader = PdfReader(pdf_file)
                pdf_text = ""
                for page in pdf_reader.pages:
                    pdf_text += page.extract_text()
                # get centralized embeddings and vector store
                with st.spinner("Generating embeddings"):
                    _embeddings = get_embeddings_pdf()
                vector_store = get_vector_store_pdf(_embeddings)
                # check if the vector store is already initialized for this PDF
                if not is_vector_store_initialized_pdf(vector_store, pdf_file.name):
                    with st.spinner("Initializing vector"):
                        vector_store = initialize_vector_store_pdf(pdf_file.name, pdf_text, vector_store)
                else:
                    pass
                query = st.text_input("Enter your query:")  # ask for user input
                if query:
                    with st.spinner("Generating response"):
                        result = query_vector_store_pdf(vector_store, query, pdf_file.name)
                        st.write(result)
            except Exception as e:
                st.error(f"An error occurred: {e}")
