# from secret_key import sec_key  # secret_key used for API call
import streamlit as st
import os  # for setting environment variable
from langchain_core.prompts import PromptTemplate  # for defining a fixed prompt
from groq import Groq  # for using LLM

sec_key = st.secrets["GROQ_API_KEY"]
langsmith_sec_key = st.secrets['LANGCHAIN_API_KEY']
os.environ['GROQ_API_KEY'] = sec_key  # secret_key set as environment variable
os.environ['LANGCHAIN_API_KEY'] = langsmith_sec_key
os.environ['LANGCHAIN_TRACING_V2'] = "true"
os.environ['LANGCHAIN_PROJECT'] = "AI Assistant"

client = Groq(api_key=sec_key)  # initialize the groq client
conversation_history = []  # store conversation history


def generate_question_and_answers(query):  # function to generate prompt
    global conversation_history  # access the global conversation history
    MAX_HISTORY = 3
    conversation_history = conversation_history[-MAX_HISTORY:]  # keep only the last 3 exchanges to reduce token usage
    history = "\n".join([f"User: {q}\nAI: {r}" for q, r in conversation_history])
    template = """  
    {history}
    User: {query}
    AI: Generate at least 10 questions and answers based on the text. Only return Q1&A1 pairs.
    """
    prompt_template = PromptTemplate(template=template, input_variables=["history", "query"])
    final_prompt = prompt_template.format(history=history, query=query)
    # call the groq llm api
    response = client.chat.completions.create(
        model="qwen-2.5-32b",
        messages=[{"role": "system", "content": final_prompt}],
        temperature=0,
        max_tokens=1024,
        top_p=0,
        stop=None
    )
    response_text = response.choices[0].message.content.strip()
    conversation_history.append((query, response_text))  # update conversation history
    return response_text


if __name__ == "__main__":
    question = "Machine learning."
    print(generate_question_and_answers(question))  # for testing purposes

