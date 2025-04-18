# from secret_key import sec_key  # secret_key used for API call
import streamlit as st
import os  # for setting environment variable
from langchain_core.prompts import PromptTemplate  # for defining a fixed prompt
from groq import Groq  # for using LLM
import re

sec_key = st.secrets["GROQ_API_KEY"]
os.environ['GROQ_API_KEY'] = sec_key  # secret_key set as environment variable

client = Groq(api_key=sec_key)  # initialize the groq client
conversation_history = []  # store conversation history


def generate_prompt(query):
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
    final_prompt = prompt_template.format(history=history, query=query)
    # call the groq llm api
    response = client.chat.completions.create(
        model="qwen-qwq-32b",
        messages=[{"role": "system", "content": final_prompt}],
        temperature=0,
        max_tokens=1024,
        top_p=0,
        stop=None
    )
    response_text = response.choices[0].message.content.strip()
    # remove content within <think>...</think> tags
    response_text = re.sub(r"<think>.*?</think>", "", response_text, flags=re.DOTALL).strip()
    conversation_history.append((query, response_text))  # update conversation history
    return response_text


if __name__ == "__main__":  # for testing purpose
    print(generate_prompt("What is 5+5"))
    print(generate_prompt("What is the square of that result?"))
