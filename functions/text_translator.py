# from secret_key import sec_key  # secret_key used for API call
import streamlit as st
import re
import os  # for setting environment variable
from langchain_core.prompts import PromptTemplate  # for defining a fixed prompt
from langchain_groq import ChatGroq  # for using LLM

sec_key = st.secrets["GROQ_API_KEY"]
# os.environ['GROQ_API_KEY'] = sec_key  # secret_key set as environment variable
langsmith_sec_key = st.secrets["LANGSMITH_API_KEY"]
os.environ["LANGSMITH_API_KEY"] = langsmith_sec_key
os.environ['LANGCHAIN_TRACING_V2'] = "true"
os.environ['LANGCHAIN_PROJECT'] = "AI Assistant"

model_name = "qwen-qwq-32b"  # model name
llm = ChatGroq(  # create the llm
    model_name=model_name,
    temperature=0,
    groq_api_key=sec_key,
    stop=None,
    model_kwargs={"top_p": 0},
    max_tokens=None,
    timeout=None,
    max_retries=2
)


def translate_text(query, target_lang):  # function to translate text
    template = f"""  
    User: {query}
    AI: You are a helpful text translator. Translate the query to {target_lang}. Do not provide anything else."
    """
    prompt_template = PromptTemplate(template=template, input_variables=["query", "target_lang"])
    sequence = prompt_template | llm
    response = sequence.invoke({"query": query, "target_lang": target_lang}).content
    response_text = re.sub(r"<think>.*?</think>", "", response, flags=re.DOTALL).strip()
    return response_text


if __name__ == "__main__":
    user_input = "I like to watch anime"
    response = translate_text(user_input, "Japanese")    # get the AI's response
    print(response)
