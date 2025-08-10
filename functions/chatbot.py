# from secret_key import sec_key, langsmith_sec_key  # secret_key used for API call
import streamlit as st
import os  # for setting environment variable
from langchain_groq import ChatGroq  # for using LLM
from langgraph.graph import StateGraph, START, END
from typing import Annotated, Sequence, Dict, List
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
    snippet: str = ""


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
    return snippet or "No relevant results found."


def invoke_duckduckgo(state: AgentState) -> dict[str, str | Sequence[BaseMessage]]:
    """ Function to invoke DuckDuckGo search and update the state """
    query = state.messages[-1].content  # get the latest user query
    search_result = duckduckgosearch(query)
    return {
        "messages": state.messages,
        "snippet": search_result
    }


def generate_prompt(state: AgentState) -> dict[str, str | list[BaseMessage]]:
    """ Function to generate prompt based on the provided search result """
    system_prompt = SystemMessage(
        content=(
            "You are a helpful AI assistant. You are given text extracted from a web search "
            "related to the user's query. Your job is to rewrite it into a clear, concise, "
            "and human-friendly answer while keeping all factual content intact. "
            "You may rephrase for readability, but do not add information that is not "
            "explicitly present in the given text. "
            "Avoid mentioning phrases like 'According to the search results' or referencing the source. "
            "If the given text is incomplete or unclear, answer with only what is available."
        )
    )
    response = llm.invoke([system_prompt] + state.messages)
    return {
        "messages": [response],
        "snippet": state.snippet
    }


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


def get_result(query: str, chat_history=None):
    if chat_history is None:
        chat_history = []
    chat_history.append(HumanMessage(content=query))  # add the new user query
    chat_history = chat_history[-3:]   # trim history to last 3 messages
    inputs = {     # prepare input for the agent
        "messages": chat_history,
        "snippet": ""
    }
    result = app.invoke(inputs)  # run the agent
    ai_messages = [  # extract AI messages
        message.content
        for message in result["messages"]
        if isinstance(message, AIMessage)
    ]
    recent_message = ai_messages[-1]
    recent_message = re.sub(r"<think>.*?</think>", "", recent_message, flags=re.DOTALL).strip()
    chat_history.append(AIMessage(content=recent_message))  # add AI response to history
    chat_history = chat_history[-3:]   # keep only the last 3 messages in history
    return recent_message, chat_history


if __name__ == "__main__":
    chat_history = []
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        response, chat_history = get_result(user_input, chat_history)
        print(response)
