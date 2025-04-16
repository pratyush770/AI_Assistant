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
    final_prompt = prompt_template.format(history=history, code_snippet=code_snippet)
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
    conversation_history.append((code_snippet, response_text))  # update conversation history
    return response_text


if __name__ == "__main__":
    print(code_assistant("print(10+"))  # for testing purposes

