# from secret_key import sec_key  # secret_key used for api call
import os  # for setting environment variable
import streamlit as st
from langchain_core.prompts import PromptTemplate  # for defining a fixed prompt
from langchain.schema.runnable import RunnableSequence  # for sequencing the flow
from langchain_groq import ChatGroq  # for using llm
from langchain.memory import ConversationBufferWindowMemory

sec_key = st.secrets["GROQ_API_KEY"]
os.environ['GROQ_API_KEY'] = sec_key  # secret_key set as environment variable
memory = ConversationBufferWindowMemory(K=5)

model_name = "mixtral-8x7b-32768"  # name of model used
llm = ChatGroq(
    model_name=model_name,
    temperature=0.6,  # more accurate results
    groq_api_key=sec_key
)


def grammar_check(query):  # function to check grammatical errors
    template = f"""  
    Question: {query}
    Check for grammatical errors and provide the most relevant an concise answer.
    Conversation so far:
    {memory.load_memory_variables({})["history"]}
    """
    prompt = PromptTemplate(template=template, input_variables=["query"])
    sequence = RunnableSequence(first=prompt, last=llm)
    response = sequence.invoke({"query": query})
    memory.save_context({"input": query}, {"output": response.content})  # save the response in memory
    return response.content  # return only the content


if __name__ == "__main__":
    print(grammar_check("I is pratyush majumdar"))  # for testing purposes
