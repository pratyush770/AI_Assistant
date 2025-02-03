# from secret_key import sec_key  # secret_key used for api call
import os  # for setting environment variable
import streamlit as st
from langchain_core.prompts import PromptTemplate  # for defining a fixed prompt
from langchain_groq import ChatGroq  # for using llm

sec_key = st.secrets["GROQ_API_KEY"]
langsmith_sec_key = st.secrets['LANGCHAIN_API_KEY']
os.environ['GROQ_API_KEY'] = sec_key  # secret_key set as environment variable
os.environ['LANGCHAIN_API_KEY'] = langsmith_sec_key
os.environ['LANGCHAIN_TRACING_V2'] = "true"  # to trace the output
os.environ['LANGCHAIN_PROJECT'] = "AI Assistant"  # project name

model_name = "mixtral-8x7b-32768"  # name of model used
llm = ChatGroq(
    model_name=model_name,
    temperature=0.6,  # more accurate results
    groq_api_key=sec_key,
)

conversation_history = []  # initialize conversation history


def code_assistant(code_snippet, reason):  # function for code assistance
    global conversation_history  # access the global conversation history
    history = "\n".join([f"User: {q}\nAI: {r}" for q, r in conversation_history])
    template = f"""
    {history}
    Code Snippet: {code_snippet}
    Question: {reason}
    Provide the most relevant and concise answer for the issue with the code snippet.
    """

    prompt_template = PromptTemplate(template=template, input_variables=["code_snippet", "reason"])
    sequence = prompt_template | llm
    response = sequence.invoke({"code_snippet": code_snippet, "reason": reason})
    response_text = response.content.strip()
    conversation_history.append((reason, response_text))  # update conversation history
    return response_text  # return only the content


if __name__ == "__main__":
    print(code_assistant("print(10+", "Why is it not working properly?"))  # for testing purposes