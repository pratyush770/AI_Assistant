# from secret_key import sec_key, langsmith_sec_key # secret_key used for API call
import streamlit as st
import os  # for setting environment variable
from langchain_core.prompts import PromptTemplate  # for defining a fixed prompt
from langchain_groq import ChatGroq  # for using LLM
import re

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
    max_tokens=1024
)

conversation_history = []  # store conversation history


def generate_prompt(query):  # function to generate prompt
    global conversation_history
    MAX_HISTORY = 3
    conversation_history = conversation_history[-MAX_HISTORY:]  # keep only the last 3 exchanges
    history = "\n".join([f"User: {q}\nAI: {r}" for q, r in conversation_history])
    polite_messages = {"thanks", "thank you", "thx", "appreciate it", "ty", "okay thanks", "thnx", "okay thank you"}
    if query.lower() in polite_messages:
        return "You're welcome! Let me know if you need anything else."
    template = """  
    {history}
    User: {query}
    AI: Provide the most relevant and concise answer. 
    """
    prompt_template = PromptTemplate(template=template, input_variables=["history", "query"])
    sequence = prompt_template | llm
    response = sequence.invoke({"history": history, "query": query}).content
    response_text = re.sub(r"<think>.*?</think>", "", response, flags=re.DOTALL).strip()
    conversation_history.append((query, response_text))  # update conversation history
    return response_text


if __name__ == "__main__":  # for testing purpose
    print(generate_prompt("What is 5+5"))
    print(generate_prompt("What is the square of that result?"))
