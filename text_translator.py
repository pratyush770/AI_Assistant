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

model_name = "mixtral-8x7b-32768"  # name of model used
llm = ChatGroq(
    model_name=model_name,
    temperature=0.6,  # more accurate results
    groq_api_key=sec_key,
)

conversation_history = []  # initialize conversation history


def translate_text(query, target_lang):  # function to translate the text
    global conversation_history  # access the global conversation history
    history = "\n".join([f"User: {q}\nAI: {r}" for q, r in conversation_history])
    template = f"""
    {history}
    Question: {query}
    Translate the following text into {target_lang}.
    Provide only the translated text.
    """

    prompt_template = PromptTemplate(template=template, input_variables=["history", "query", "target_lang"])
    sequence = prompt_template | llm
    response = sequence.invoke({"history": history, "query": query, "target_lang": target_lang})
    response_text = response.content.strip()
    conversation_history.append((query, response_text))  # update conversation history
    return response_text  # return only the content


if __name__ == "__main__":
    print(translate_text("I like to watch anime", "Japanese"))  # for testing purposes
