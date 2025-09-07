from fastapi import FastAPI
from pydantic import BaseModel
from chatbot import chatbot
from langchain_core.messages import HumanMessage

app = FastAPI()

class ChatRequest(BaseModel):
    user_id: str
    message: str

@app.post("/chat")
def chat(request: ChatRequest):
    # user_id as thread_id for persistence
    config = {"configurable": {"thread_id": request.user_id}}
    
    # Call chatbot
    response = chatbot.invoke({"messages": [HumanMessage(content=request.message)]}, config)
    
    return {"reply": response["messages"][-1].content}
