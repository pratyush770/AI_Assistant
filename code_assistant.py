# from secret_key import sec_key  # secret_key used for API call
import os  # for setting environment variable
import streamlit as st
from langchain_core.prompts import PromptTemplate  # for defining a fixed prompt
from langchain_groq import ChatGroq  # for using LLM

sec_key = st.secrets["GROQ_API_KEY"]
langsmith_sec_key = st.secrets['LANGCHAIN_API_KEY']
os.environ['GROQ_API_KEY'] = sec_key  # secret_key set as environment variable
os.environ['LANGCHAIN_API_KEY'] = langsmith_sec_key
os.environ['LANGCHAIN_TRACING_V2'] = "true"
os.environ['LANGCHAIN_PROJECT'] = "AI Assistant"

model_name = "qwen-2.5-32b"
llm = ChatGroq(
    model_name=model_name,
    temperature=0.3,
    groq_api_key=sec_key,
)

conversation_history = []  # initialize conversation history


@st.cache_data(show_spinner=False)
def code_assistant(code_snippet):  # function for code assistance
    global conversation_history
    MAX_HISTORY = 3
    conversation_history = conversation_history[-MAX_HISTORY:]  # keep only the last 3 exchanges to reduce token usage
    history = "\n".join([f"User: {q}\nAI: {r}" for q, r in conversation_history])
    template = """
    {history}
    Code Snippet: {code_snippet}
    Provide the most relevant and concise answer for the issue with the code snippet.
    """
    prompt_template = PromptTemplate(template=template, input_variables=["history", "code_snippet"])
    sequence = prompt_template | llm
    response = sequence.invoke({"history": history, "code_snippet": code_snippet})
    response_text = response.content.strip()
    conversation_history.append((code_snippet, response_text))
    return response_text  # return only the content


if __name__ == "__main__":
    print(code_assistant("print(10+"))  # for testing purposes
