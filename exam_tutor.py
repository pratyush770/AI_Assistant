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
    groq_api_key=sec_key,
)


def generate_question_and_answers(query):  # function to generate prompt
    template = f"""  
    Question: {query}
    Generate questions based on the text and give answers to each questions too.
    Conversation so far:
    {memory.load_memory_variables({})["history"]}
    """
    prompt_template = PromptTemplate(template=template, input_variables=["query"])
    sequence = RunnableSequence(first=prompt_template, last=llm)
    response = sequence.invoke({"query": query})
    memory.save_context({"input": query}, {"output": response.content})
    return response.content  # return only the content


if __name__ == "__main__":
    question = """
    Machine learning is a subset of Artificial Intelligence (AI) that enables computers to learn from data and make predictions without being explicitly programmed. 
    Machine learning can be broadly categorized into three types:
    Supervised Learning: Trains models on labeled data to predict or classify new, unseen data.
    Unsupervised Learning: Finds patterns or groups in unlabeled data, like clustering or dimensionality reduction.
    Reinforcement Learning: Learns through trial and error to maximize rewards, ideal for decision-making tasks.
    Machine learning is fundamentally built upon data, which serves as the foundation for training and testing models. Data consists of inputs (features) and outputs (labels). A model learns patterns during training and is tested on unseen data to evaluate its performance and generalization. In order to make predictions, there are essential steps through which data passes in order to produce a machine learning model that can make predictions.
    """
    print(generate_question_and_answers(question))  # for testing purposes

