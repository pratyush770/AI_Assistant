# from secret_key import sec_key, langsmith_sec_key  # secret_key used for API call
import streamlit as st
import os  # for setting environment variable
from langchain_groq import ChatGroq  # for using LLM
from langgraph.graph import StateGraph, START, END
from typing import Annotated, Sequence
from pydantic import BaseModel
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage, SystemMessage, AIMessage, HumanMessage
import re
from ddgs import DDGS

sec_key = st.secrets["GROQ_API_KEY"]
# os.environ['GROQ_API_KEY'] = sec_key  # secret_key set as environment variable
langsmith_sec_key = st.secrets["LANGSMITH_API_KEY"]
os.environ["LANGSMITH_API_KEY"] = langsmith_sec_key
os.environ['LANGCHAIN_TRACING_V2'] = "true"
os.environ['LANGCHAIN_PROJECT'] = "AI Assistant"


class AgentState(BaseModel):
    messages: Annotated[Sequence[BaseMessage], add_messages]


model_name = "qwen/qwen3-32b"  # model name
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


def duckduckgosearch(input: str) -> str:
    """ Function to search user's input using DDGS and return the result.
    Parameter:
        input -> user input
    """
    result = DDGS().text(query=input, num_results=1, backend="auto")
    snippet = next((r["body"] for r in result if "body" in r), None)
    return snippet


def invoke_duckduckgo(state: AgentState) -> AgentState:
    """ Function to invoke DuckDuckGo search and update the state """
    query = state.messages[-1].content  # get the latest user query
    search_result = duckduckgosearch(query)
    # append the search results as a new message in the chat history
    updated_messages = state.messages + [SystemMessage(content=search_result)]
    return {"messages": updated_messages}


def generate_prompt(state: AgentState) -> AgentState:
    """ Function to generate prompt based on the provided search result """
    system_prompt = SystemMessage(
        content="You are a helpful AI assistant. Your task is to generate a concise and humanized response "
                "based strictly on the provided search results. Do not add any extra information, reasoning, "
                "or commentary beyond what is explicitly stated in the search results. "
                "Don't mention words like 'search results' in the response")
    message = [system_prompt] + state.messages
    response = llm.invoke(message)
    return {"messages": [response]}


graph = StateGraph(AgentState)
graph.add_node("invoke_duckduckgo", invoke_duckduckgo)  # node to invoke DuckDuckGo search
graph.add_node("generate_response", generate_prompt)
graph.add_edge(START, "invoke_duckduckgo")
graph.add_edge("invoke_duckduckgo", "generate_response")
graph.add_edge("generate_response", END)
app = graph.compile()

# image_path = "chatbot_graph.png"  # image path
# with open(image_path, "wb") as f:
#     f.write(app.get_graph().draw_mermaid_png())  # get the graph image


def get_result(query, chat_history=None):
    if chat_history is None:
        chat_history = []  # initialize an empty chat history if none is provided
    chat_history.append(HumanMessage(content=query))  # append the user's query to the chat history
    chat_history = chat_history[-3:]   # trim the chat history to the last 3 messages
    inputs = {"messages": chat_history}  # prepare the input for the agent
    result = app.invoke(inputs)  # invoke the agent with the updated chat history
    # extract the AI's response
    ai_messages = [
        message.content if isinstance(message, AIMessage) else str(message)
        for message in result["messages"]
        if isinstance(message, AIMessage)
    ]
    recent_message = ai_messages[-1]  # get the recent message
    recent_message = re.sub(r"<think>.*?</think>", "", recent_message, flags=re.DOTALL).strip()
    chat_history.append(AIMessage(content=recent_message))
    chat_history = chat_history[-3:]  # trim the chat history again to ensure it contains only the last 3 messages
    return recent_message, chat_history  # return the most recent AI response and the updated chat history


if __name__ == "__main__":
    chat_history = []  # initialize an empty chat history
    while True:  # example interaction loop
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        response, chat_history = get_result(user_input, chat_history)    # get the AI's response and update the chat history
        print(response)
