# from secret_key import sec_key  # secret_key used for API call
import streamlit as st
import os  # for setting environment variable
from langchain_groq import ChatGroq  # for using LLM
from langgraph.graph import StateGraph, START, END
from typing import Annotated, Sequence
from pydantic import BaseModel
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage, SystemMessage, AIMessage
from langgraph.prebuilt import ToolNode
from functions.tools import bravesearch, add_numbers, subtract_numbers, multiply_numbers, divide_numbers

sec_key = st.secrets["GROQ_API_KEY"]
# os.environ['GROQ_API_KEY'] = sec_key  # secret_key set as environment variable
langsmith_sec_key = st.secrets["LANGSMITH_API_KEY"]
os.environ["LANGSMITH_API_KEY"] = langsmith_sec_key
os.environ['LANGCHAIN_TRACING_V2'] = "true"
os.environ['LANGCHAIN_PROJECT'] = "AI Assistant"


class AgentState(BaseModel):
    messages: Annotated[Sequence[BaseMessage], add_messages]


tools = [bravesearch, add_numbers, subtract_numbers, multiply_numbers, divide_numbers]

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
).bind_tools(tools)


def generate_prompt(state: AgentState) -> AgentState:
    """ Function to generate prompt """
    system_prompt = SystemMessage(
        content="You are a helpful code assistant. Use the provided tools to fetch real-time data when necessary."
                " If no tool is required, provide the most relevant and concise answer for the issue with the code snippet."
    )
    message = [system_prompt] + state.messages
    response = llm.invoke(message)
    return {"messages": [response]}


def should_continue(state: AgentState) -> str:
    """ Function to decide the next flow of execution """
    messages = state.messages
    last_message = messages[-1]  # get the most recent message
    if not last_message.tool_calls:  # if there is no further tool calls
        return "response"  # return the edge
    else:
        return "continue"


graph = StateGraph(AgentState)
graph.add_node("llm", generate_prompt)
tool_node = ToolNode(tools=tools)  # create ToolNode
graph.add_node("tools", tool_node)
graph.add_edge(START, "llm")
graph.add_conditional_edges(
    "llm",
    should_continue,
    {
        "continue": "tools",
        "response": END
    }
)
graph.add_edge("tools", "llm")  # goes back from tool node to our agent node
app = graph.compile()


def get_code(query):
    inputs = {"messages": query}  # prepare the input for the agent
    result = app.invoke(inputs)  # invoke the agent with the updated chat history
    # extract the AI's response
    ai_messages = [
        message.content if isinstance(message, AIMessage) else str(message)
        for message in result["messages"]
        if isinstance(message, AIMessage)
    ]
    recent_message = ai_messages[-1]  # get the recent message
    return recent_message  # return the most recent AI response


if __name__ == "__main__":
    user_input = "print(a + 10)"
    response = get_code(user_input)    # get the AI's response and update the chat history
    print(response)

