from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_groq import ChatGroq
from vectordb import retriever
from dotenv import load_dotenv

load_dotenv()


# Initialize LLM
llm = ChatGroq(model="meta-llama/llama-4-maverick-17b-128e-instruct")

# State
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

# Node with FAQ + RAG fallback
def chat_node(state: ChatState):
    messages = state["messages"]
    user_message = messages[-1].content

    # Step 1: Try retrieving relevant docs
    docs = retriever.invoke(user_message)
    if docs:
        context = " ".join([d.page_content for d in docs])
        prompt = f"""
                        You are Iron Lady's assistant.
                        Context: {context}

                        Conversation so far:
                        {[m.content for m in messages]}

                        User's Question: {user_message}
                        Answer clearly and concisely:
                        If you dont know the answer, Simply say I dont have that information.
                    """
        response = llm.invoke([HumanMessage(content=prompt)])
        answer = response.content
    else:
        # Step 2: Use full conversation history as fallback
        response = llm.invoke(messages)
        answer = response.content

    return {"messages": [AIMessage(content=answer)]}
# Persistence
checkpointer = MemorySaver()

# Build graph
graph = StateGraph(ChatState)
graph.add_node("chat_node", chat_node)
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

# Compile chatbot
chatbot = graph.compile(checkpointer=checkpointer)