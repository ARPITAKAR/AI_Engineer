from langgraph.graph import StateGraph,START,END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import InMemorySaver
import os
from dotenv import load_dotenv

load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

llm_endpoint = HuggingFaceEndpoint(
    repo_id= "Qwen/Qwen3-4B-Instruct-2507",
    huggingfacehub_api_token=HF_TOKEN,
    task="text-generation",
    max_new_tokens=400,
    temperature=0.6, top_p=0.95, top_k=20
    )

llm = ChatHuggingFace(llm=llm_endpoint)

class ChatState(TypedDict):
    # BaseMessage is the mother class [HumanMessage,AImessage,Toolmessage,SystemMessage]
    messages : Annotated[list[BaseMessage],add_messages]

def chat_node(state:ChatState):
    messages = state['messages']
    response = llm.invoke(messages)
    return {"messages": [response]}
    
# Checkpointer
checkpointer = InMemorySaver()

graph = StateGraph(ChatState)
graph.add_node("chat_node",chat_node)

graph.add_edge(START,"chat_node")
graph.add_edge("chat_node",END)

chatbot = graph.compile(checkpointer=checkpointer)