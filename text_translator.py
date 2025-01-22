from secret_key import sec_key  # secret_key used for api call
import os  # for setting environment variable
import streamlit as st
from langchain_core.prompts import PromptTemplate  # for defining a fixed prompt
from langchain.schema.runnable import RunnableSequence  # for sequencing the flow
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
    groq_api_key=sec_key
)


def translate_text(query, target_lang):  # function to translate the text
    template = f"""
    Question: {query}
    Translate the following text into {target_lang}.
    Provide only the translated text and not any other information.
    """
    prompt = PromptTemplate(template=template, input_variables=["query", "target_lang"])
    sequence = RunnableSequence(first=prompt, last=llm)
    response = sequence.invoke({"query": query, "target_lang": target_lang})
    return response.content  # return only the content


if __name__ == "__main__":
    print(translate_text("I like to watch anime", "Japanese"))  # for testing purposes
