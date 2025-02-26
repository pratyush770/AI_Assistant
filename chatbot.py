# from secret_key import sec_key  # secret_key used for api call
import streamlit as st
import os  # for setting environment variable
from langchain_core.prompts import PromptTemplate  # for defining a fixed prompt
from langchain_groq import ChatGroq  # for using llm

sec_key = st.secrets["GROQ_API_KEY"]
langsmith_sec_key = st.secrets['LANGCHAIN_API_KEY']
os.environ['GROQ_API_KEY'] = sec_key  # secret_key set as environment variable
os.environ['LANGCHAIN_API_KEY'] = langsmith_sec_key
os.environ['LANGCHAIN_TRACING_V2'] = "true"  # to trace the output
os.environ['LANGCHAIN_PROJECT'] = "AI Assistant"  # project name

model_name = "gemma2-9b-it"  # name of model used
llm = ChatGroq(
    model_name=model_name,
    temperature=0.3,  # more accurate results
    groq_api_key=sec_key
)

conversation_history = []  # initialize conversation history


@st.cache_data(show_spinner=False)
def generate_prompt(query):  # function to generate prompt
    global conversation_history  # access the global conversation history
    MAX_HISTORY = 3
    conversation_history = conversation_history[-MAX_HISTORY:]  # keep only the last 3 exchanges to reduce token usage
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
    response = sequence.invoke({"history": history, "query": query})
    response_text = response.content.strip()
    conversation_history.append((query, response_text))  # update conversation history
    return response_text  # return only the content


if __name__ == "__main__":
    print(generate_prompt("What is 5+5"))  # for testing purposes
    print(generate_prompt("What is the square of that result?"))  # testing follow-up
